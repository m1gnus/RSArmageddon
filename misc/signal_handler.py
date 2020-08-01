import signal
import sys
import os

"""
This will contain the PID of the processes that will be terminated
"""
pids = []

"""
signal to send to the processes which pids is specified in "pids"
"""
signal_ = signal.SIGTERM

def signal_name(signalNumber: int) -> str:
    signals = ["SIGHUP", "SIGINT", "SIGQUIT", "SIGILL", "SIGTRAP", "SIGABRT", "SIGBUS", "SIGFPE", "SIGKILL", "SIGUSR1", "SIGSEGV", "SIGUSR2", "SIGPIPE", "SIGALRM", "SIGTERM", "SIGSTKFLT", "SIGCHLD", "SIGCONT", "SIGSTOP", "SIGTSTP", "SIGTTIN", "SIGTTOU", "SIGURG", "SIGXCPU", "SIGXFSZ", "SIGVTALRM", "SIGPROF", "SIGWINCH", "SIGIO", "SIGPWR", "SIGSYS", "SIGRTMIN", "SIGRTMIN+1", "SIGRTMIN+2", "SIGRTMIN+3", "SIGRTMIN+4", "SIGRTMIN+5", "SIGRTMIN+6", "SIGRTMIN+7", "SIGRTMIN+8", "SIGRTMIN+9", "SIGRTMIN+10", "SIGRTMIN+11", "SIGRTMIN+12", "SIGRTMIN+13", "SIGRTMIN+14", "SIGRTMIN+15", "SIGRTMAX-14", "SIGRTMAX-13", "SIGRTMAX-12", "SIGRTMAX-11", "SIGRTMAX-10", "SIGRTMAX-9", "SIGRTMAX-8", "SIGRTMAX-7", "SIGRTMAX-6", "SIGRTMAX-5", "SIGRTMAX-4", "SIGRTMAX-3", "SIGRTMAX-2", "SIGRTMAX-1", "SIGRTMAX"]
    return signals[signalNumber - 1]

def kill_processes(signalNumber: int, frame: str) -> None:
    global pids
    print("\n[.] received a signal ->", signal_name(signalNumber))
    print("sending", signal_name(signal_), "to the following processes:", pids)
    for pid in pids:
        os.kill(pid, signal_)
    sys.exit(0)

"""
signal to catch, if you don't want to catch one of this signals comment the relative line
"""
signal.signal(signal.SIGHUP, kill_processes)
signal.signal(signal.SIGINT, kill_processes)
signal.signal(signal.SIGQUIT, kill_processes)
signal.signal(signal.SIGILL, kill_processes)
signal.signal(signal.SIGTRAP, kill_processes)
signal.signal(signal.SIGABRT, kill_processes)
signal.signal(signal.SIGBUS, kill_processes)
signal.signal(signal.SIGFPE, kill_processes)
signal.signal(signal.SIGUSR1, kill_processes)
signal.signal(signal.SIGSEGV, kill_processes)
signal.signal(signal.SIGUSR2, kill_processes)
signal.signal(signal.SIGPIPE, kill_processes)
signal.signal(signal.SIGTERM, kill_processes)