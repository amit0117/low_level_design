# 🛠️ Node.js Architecture: Event Loop, Concurrency & Worker Threads

This guide covers how Node.js handles thousands of requests, manages asynchronous I/O via Libuv, and processes CPU-heavy tasks without blocking the main thread.

---

## 🌍 1. Browser vs. Node.js Architecture

While both use the V8 Engine, they provide different environments for the Event Loop.

| Feature | Web Browser | Node.js (Backend) |
| :--- | :--- | :--- |
| Provider | Browser Web APIs | Libuv (C library) |
| Standard | HTML5 Spec | Custom Libuv implementation |
| Main Goal | Smooth UI & Rendering | High-throughput I/O |

---

## 🟢 2. The Node.js Event Loop (6 Phases)

Node.js organizes callbacks into 6 distinct phases. Each phase has its own FIFO queue.

### 🔄 The Loop Order

1. Timers: setTimeout() and setInterval()
2. Pending Callbacks: System-level I/O errors (e.g., TCP connection refused)
3. Idle, Prepare: Internal Node.js housekeeping
4. Poll (The Heart): Retrieves new I/O events. If the queue is empty, the loop "blocks" (sleeps) here
5. Check: setImmediate() callbacks
6. Close Callbacks: socket.on('close'), etc

---

## ⚡ 3. The Microtask Queue: The "VIP" Interrupt

Microtasks (Promises, process.nextTick) are not a phase. They are a high-priority interrupt.

- Draining: The loop stops after every single callback and between every phase to execute every waiting Microtask until the queue is empty
- Priority: process.nextTick queue is drained before the Promise queue

---

## 🚀 4. I/O Multiplexing (Handling 100k+ Requests)

Node.js uses Non-blocking I/O to handle massive concurrency on a single thread.

1. Delegation: Node asks the OS (epoll on Linux) to watch thousands of sockets
2. Sleep: The Event Loop enters the Poll Phase and sleeps
3. Wake-up: When data arrives, the OS wakes the loop
4. Efficiency: The CPU only works when there is code to run, not while waiting for the network

---

## 🧠 5. CPU-Heavy Tasks & Worker Threads

If you perform a heavy calculation (e.g., Image Processing, Password Hashing) on the Main Thread, the Event Loop freezes. No other requests can be handled.

### ✅ The Solution: worker_threads

For CPU-bound tasks, use the worker_threads module to spawn separate threads that have their own V8 instance and Event Loop.

- Main Thread: Handles I/O and HTTP requests
- Worker Thread: Handles heavy computation
- Communication: Message passing (postMessage)

---

## 📝 6. Technical Quiz: Execution Order

Question: What is the output of this code?

Code:

const fs = require('fs');

console.log('1: Start');

setTimeout(() => console.log('2: Timeout'), 0);

fs.readFile(__filename, () => {
    console.log('3: File Read');
    setTimeout(() => console.log('4: Inner Timeout'), 0);
    setImmediate(() => console.log('5: Inner Immediate'));
    process.nextTick(() => console.log('6: Inner NextTick'));
});

Promise.resolve().then(() => console.log('7: Promise'));

console.log('8: End');

---

### 💡 Answer, Output & Explanation (All Together)

Output:

1: Start
8: End
7: Promise
2: Timeout
3: File Read
6: Inner NextTick
5: Inner Immediate
4: Inner Timeout

Explanation:

1. 1: Start (Sync)
2. 8: End (Sync)
3. 7: Promise (Microtask - runs after sync code)
4. 2: Timeout (Timers phase)
5. 3: File Read (Poll phase)
6. 6: Inner NextTick (Microtask - runs immediately after callback)
7. 5: Inner Immediate (Check phase)
8. 4: Inner Timeout (Next loop - Timers phase)

---

## 📌 Critical Revision Summary

- Infrastructure: Event Loop is provided by Libuv, not V8
- Microtask Logic: Microtasks drain between every callback
- The Heart: Poll Phase is where Node waits for new requests
- Work Division: Worker Threads are for CPU, Event Loop is for I/O
- Golden Rule: Do not block the Event Loop