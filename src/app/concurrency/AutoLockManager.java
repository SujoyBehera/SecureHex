package app.concurrency;

import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicLong;
import javax.swing.SwingUtilities;

/**
 * <h1>Concurrent Auto-Lock Manager</h1>
 * <p>Demonstrating Syllabus <b>Unit-3: Concurrent Programming Paradigm - Multithreading and Multitasking</b>.</p>
 * <p>
 * Uses a dedicated background daemon {@link Thread} that tracks inactivity period
 * and triggers a vault lock without blocking user interface responsiveness.
 * </p>
 *
 * @author SecureHex Development Team (Group of 3)
 */
public class AutoLockManager implements Runnable {

    private final long timeoutMillis;
    private final Runnable lockCallback;
    private final AtomicLong lastActivityTime;
    private final AtomicBoolean isRunning;
    private Thread monitorThread;

    /**
     * Initializes the auto-lock manager.
     *
     * @param timeoutSeconds Inactivity timeout in seconds
     * @param lockCallback Callback executed when inactivity threshold is exceeded
     */
    public AutoLockManager(int timeoutSeconds, Runnable lockCallback) {
        this.timeoutMillis = timeoutSeconds * 1000L;
        this.lockCallback = lockCallback;
        this.lastActivityTime = new AtomicLong(System.currentTimeMillis());
        this.isRunning = new AtomicBoolean(false);
    }

    /**
     * Starts the concurrency monitor thread.
     */
    public synchronized void start() {
        if (!isRunning.get()) {
            isRunning.set(true);
            lastActivityTime.set(System.currentTimeMillis());
            monitorThread = new Thread(this, "SecureHex-AutoLock-Daemon");
            monitorThread.setDaemon(true); // Daemon thread exits when main application terminates
            monitorThread.start();
        }
    }

    /**
     * Stops the monitor thread safely.
     */
    public synchronized void stop() {
        isRunning.set(false);
        if (monitorThread != null) {
            monitorThread.interrupt();
        }
    }

    /**
     * Resets the inactivity timer upon detecting user interaction (mouse/keyboard events).
     */
    public void recordUserActivity() {
        lastActivityTime.set(System.currentTimeMillis());
    }

    /**
     * Gets the remaining idle seconds before locking.
     */
    public int getRemainingSeconds() {
        long elapsed = System.currentTimeMillis() - lastActivityTime.get();
        long remaining = timeoutMillis - elapsed;
        return (int) Math.max(0, remaining / 1000);
    }

    @Override
    public void run() {
        while (isRunning.get()) {
            try {
                // Sleep for 1 second intervals to monitor status
                Thread.sleep(1000);

                long elapsed = System.currentTimeMillis() - lastActivityTime.get();
                if (elapsed >= timeoutMillis) {
                    isRunning.set(false);

                    // Execute lock callback on the Swing Event Dispatch Thread (EDT)
                    if (lockCallback != null) {
                        SwingUtilities.invokeLater(lockCallback);
                    }
                    break;
                }
            } catch (InterruptedException e) {
                // Thread interrupted on shutdown
                break;
            }
        }
    }
}
