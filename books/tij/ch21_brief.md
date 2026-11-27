# 21. Concurrency (printed p797-932)


<!--p819-->

<!--p820-->

<!--p821-->

<!--p822-->

<!--p823-->
Concurrency Up to this point, you’ve been learning about sequential programming. Everything in a program happens one step at a time. A large subset of programming problems can be solved using sequential programming. For some problems, however, it becomes convenient or even essential to execute several parts of a program in parallel, so that those portions either appear to be executing concurrently, or if multiple processors are available, actually do execute simultaneously. Parallel programming can produce great improvements in program execution speed, provide an easier model for designing certain types of programs, or both. However, becoming adept at concurrent programming theory and techniques is a step up from everything you’ve learned so far in this book, and is an intermediate to advanced topic. This chapter can only serve as an introduction, and you should by no means consider yourself a good concurrent programmer even if you understand this chapter thoroughly. As you shall see, the real problem with concurrency occurs when tasks that are executing in parallel begin to interfere with each other. This can happen in such a subtle and occasional manner that it’s probably fair to say that concurrency is "arguably deterministic but effectively nondeterministic." That is, you can make an argument to conclude that it’s possible to write concurrent programs that, through care and code inspection, work correctly. In practice, however, it’s much easier to write concurrent programs that only appear to work, but given the right conditions, will fail. These conditions may never actually occur, or occur so infrequently that you never see them during testing. In fact, you may not be able to write test code that will generate failure conditions for your concurrent program. The resulting failures will often only occur occasionally, and as a result they appear in the form of customer complaints. This is one of the strongest arguments for studying concurrency: If you ignore it, you’re likely to get bitten. Concurrency thus seems fraught with peril, and if that makes you a bit fearful, this is probably a good thing. Although Java SE5 has made significant improvements in concurrency, there are still no safety nets like compile-time verification or checked exceptions to tell you when you make a mistake. With concurrency, you’re on your own, and only by being both suspicious and aggressive can you write multithreaded code in Java that will be reliable. People sometimes suggest that concurrency is too advanced to include in a book that introduces the language. They argue that concurrency is a discrete topic that can be treated independently, and the few cases where it appears in daily programming (such as graphical user interfaces) can be handled with special idioms. Why introduce such a complex topic if you can avoid it? Alas, if only it were so. Unfortunately, you don’t get to choose when threads will appear in your Java programs. Just because you never start a thread yourself doesn’t mean you’ll be able to avoid writing threaded code. For example, Web systems are one of the most common Java applications, and the basic Web library class, the servlet, is inherently multithreaded— this is essential because Web servers often contain multiple processors, and concurrency is an ideal way to utilize these processors. As simple as a servlet might seem, you must understand concurrency issues in order to use servlets properly. The same goes for graphical user interface programming, as you shall see in the Graphical User Interfaces chapter. Although the Swing and SWT libraries both have mechanisms for thread safety, it’s hard to know how to use these properly without understanding concurrency. Java is a multithreaded language, and concurrency issues are present whether you are aware of them or not. As a result, there are many Java programs in use that either just work by accident, or work most of the time and mysteriously break every now and again because of undiscovered concurrency flaws. Sometimes this breakage is benign, but sometimes it means the loss of valuable data, and if you aren’t at least aware of concurrency issues, you may end up assuming the problem is somewhere else rather than in your software. These kinds of issues can also be exposed or amplified if a program is moved to a multiprocessor system. Basically, knowing about concurrency makes you aware that apparently correct programs can exhibit incorrect behavior. Concurrent programming is like stepping into a new world and learning a new language, or at least a new set of language concepts. Understanding concurrent programming is on the same order of difficulty as understanding object-oriented programming. If you apply some effort, you can fathom the basic mechanism, but it generally takes deep study and understanding to develop a true grasp of the subject. The goal of this chapter is to give you a solid foundation in the basics of concurrency so that you can understand the concepts and write reasonable multithreaded programs. Be aware that you can easily become overconfident. If you are writing anything complex, you will need to study dedicated books on the topic. The many faces of concurrency A primary reason why concurrent programming can be confusing is that there is more than one problem to solve using concurrency, and more than one approach to implementing concurrency, and no clean mapping between the two issues (and often a blurring of the lines all around). As a result, you’re forced to understand all issues and special cases in order to use concurrency effectively. The problems that you solve with concurrency can be roughly classified as "speed" and "design manageability." Faster execution The speed issue sounds simple at first: If you want a program to run faster, break it into pieces and run each piece on a separate processor. Concurrency is a fundamental tool for multiprocessor programming. Now, with Moore’s Law running out of steam (at least for conventional chips), speed improvements are appearing in the form of multicore processors rather than faster chips. To make your programs run faster, you’ll have to learn to take advantage of those extra processors, and that’s one thing that concurrency gives you. If you have a multiprocessor machine, multiple tasks can be distributed across those processors, which can dramatically improve throughput. This is often the case with powerful multiprocessor Web servers, which can distribute large numbers of user requests across CPUs in a program that allocates one thread per request. However, concurrency can often improve the performance of programs running on a single processor. This can sound a bit counterintuitive. If you think about it, a concurrent program running on a single processor should actually have more overhead than if all the parts of the program ran sequentially, because of the added cost of the so-called context switch (changing from one task to another). On the surface, it would appear to be cheaper to run all the parts of the program as a single task and save the cost of context switching. The issue that can make a difference is blocking. If one task in your program is unable to continue because of some condition outside of the control of the program (typically I/O), we say that the task or the thread blocks. Without concurrency, the whole program comes to a stop until the external condition changes. If the program is written using concurrency, however, the other tasks in the program can continue to execute when one task is blocked, so the program continues to move forward. In fact, from a performance standpoint, it makes no sense to use concurrency on a single-processor machine unless one of the tasks might block. A very common example of performance improvements in single-processor systems is event- driven programming. Indeed, one of the most compelling reasons for using concurrency is to produce a responsive user interface. Consider a program that performs some long-running operation and thus ends up ignoring user input and being unresponsive. If you have a "quit" button, you don’t want to be forced to poll it in every piece of code you write. This produces awkward code, without any guarantee that a programmer won’t forget to perform the check. Without concurrency, the only way to produce a responsive user interface is for all tasks to periodically check for user input. By creating a separate thread of execution to respond to user input, even though this thread will be blocked most of the time, the program guarantees a certain level of responsiveness. The program needs to continue performing its operations, and at the same time it needs to return control to the user interface so that the program can respond to the user. But a conventional method cannot continue performing its operations and at the same time return control to the rest of the program. In fact, this sounds like an impossibility, as if the CPU must be in two places at once, but this is precisely the illusion that concurrency provides (in the case of multiprocessor systems, this is more than just an illusion). One very straightforward way to implement concurrency is at the operating system level, using processes. A process is a self-contained program running within its own address space. A multitasking operating system can run more than one process (program) at a time by periodically switching the CPU from one process to another, while making it look as if each process is chugging along on its own. Processes are very attractive because the operating system usually isolates one process from another so they cannot interfere with each other, which makes programming with processes relatively easy. In contrast, concurrent systems like the one used in Java share resources like memory and I/O, so the fundamental difficulty in writing multithreaded programs is coordinating the use of these resources between different thread-driven tasks, so that they cannot be accessed by more than one task at a time. Here’s a simple example that utilizes operating system processes. While writing a book, I regularly make multiple redundant backup copies of the current state of the book. I make a copy into a local directory, one onto a memory stick, one onto a Zip disk, and one onto a remote FTP site. To automate this process, I wrote a small program (in Python, but the concepts are the same) which zips the book into a file with a version number in the name and then performs the copies. Initially, I performed all the copies sequentially, waiting for each one to complete before starting the next one. But then I realized that each copy operation took a different amount of time depending on the I/O speed of the medium. Since I was using a multitasking operating system, I could start each copy operation as a separate process and let them run in parallel, which speeds up the execution of the entire program. While one process is blocked, another one can be moving forward. This is an ideal example of concurrency. Each task executes as a process in its own address space, so there’s no possibility of interference between tasks. More importantly, there’s no need for the tasks to communicate with each other because they’re all completely independent. The operating system minds all the details of ensuring proper file copying. As a result, there’s no risk and you get a faster program, effectively for free. Concurrency Some people go so far as to advocate processes as the only reasonable approach to concurrency,1but unfortunately there are generally quantity and overhead limitations to processes that prevent their applicability across the concurrency spectrum. Some programming languages are designed to isolate concurrent tasks from each other. These are generally called/imcft’onaZ languages, where each function call produces no side effects (and so cannot interfere with other functions) and can thus be driven as an independent task. Erlang is one such language, and it includes safe mechanisms for one task to communicate with another. If you find that a portion of your program must make heavy use of concurrency and you are running into excessive problems trying to build that portion, you may want to consider creating that part of your program in a dedicated concurrency language like Erlang. Java took the more traditional approach of adding support for threading on top of a sequential language.2Instead of forking external processes in a multitasking operating system, threading creates tasks within the single process represented by the executing program. One advantage that this provided was operating system transparency, which was an important design goal for Java. For example, the pre-OSX versions of the Macintosh operating system (a reasonably important target for the first versions of Java) did not support multitasking. Unless multithreading had been added to Java, any concurrent Java programs wouldn’t have been portable to the Macintosh and similar platforms, thus breaking the "write once/run everywhere" requirement.3 Improving code design A program that uses multiple tasks on a single-CPU machine is still just doing one thing at a time, so it must be theoretically possible to write the same program without using any tasks. However, concurrency provides an important organizational benefit: The design of your program can be greatly simplified. Some types of problems, such as simulation, are difficult to solve without support for concurrency. Most people have seen at least one form of simulation, as either a computer game or computer-generated animations within movies. Simulations generally involve many interacting elements, each with "a mind of its own." Although you may observe that, on a single-processor machine, each simulation element is being driven forward by that one processor, from a programming standpoint it’s much easier to pretend that each simulation element has its own processor and is an independent task. A full-fledged simulation may involve a very large number of tasks, corresponding to the fact that each element in a simulation can act independently—this includes doors and rocks, not just elves and wizards. Multithreaded systems often have a relatively small size limit on the number of threads available, sometimes on the order of tens or hundreds. This number may vary outside the control of the program—it may depend on the platform, or in the case of Java, the version of the JVM. In Java, you can generally assume that you will not have enough threads available to provide one for each element in a large simulation. A typical approach to solving this problem is the use of cooperative multithreading. Java’s threading is preemptive, which means that a scheduling mechanism provides time slices for each thread, periodically interrupting a thread and context switching to another thread so that each one is given a reasonable amount of time to drive its task. In a cooperative system, 1 Eric Raymond, for example, makes a strong case in The Art of UNIX Programming (Addison-Wesley, 2004). 2 It could be argued that trying to bolt concurrency onto a sequential language is a doomed approach, but you’ll have to draw your own conclusions. 3 This requirement was never completely fulfilled and is no longer so loudly touted by Sun. Ironically, one reason that "write once/run everywhere" didn’t completely work may have resulted from problems in the threading system—which might actually be fixed in Java SE5. Concurrency each task voluntarily gives up control, which requires the programmer to consciously insert some kind of yielding statement into each task. The advantage to a cooperative system is twofold: Context switching is typically much cheaper than with a preemptive system, and there is theoretically no limit to the number of independent tasks that can be running at once. When you are dealing with a large number of simulation elements, this can be the ideal solution. Note, however, that some cooperative systems are not designed to distribute tasks across processors, which can be very limiting. At the other extreme, concurrency is a very useful model—because it’s what is actually happening—when you are working with modern messaging systems, which involve many independent computers distributed across a network. In this case, all the processes are running completely independently of each other, and there’s not even an opportunity to share resources. However, you must still synchronize the information transfer between processes so that the entire messaging system doesn’t lose information or incorporate information at incorrect times. Even if you don’t plan to use concurrency very much in your immediate future, it’s helpful to understand it just so you can grasp messaging architectures, which are becoming more predominant ways to create distributed systems. Concurrency imposes costs, including complexity costs, but these are usually outweighed by improvements in program design, resource balancing, and user convenience. In general, threads enable you to create a more loosely coupled design; otherwise, parts of your code would be forced to pay explicit attention to tasks that would normally be handled by threads. Basic threading Concurrent programming allows you to partition a program into separate, independently running tasks. Using multithreading, each of these independent tasks (also called subtasks) is driven by a thread of execution. A thread is a single sequential flow of control within a process. A single process can thus have multiple concurrently executing tasks, but you program as if each task has the CPU to itself. An underlying mechanism divides up the CPU time for you, but in general, you don’t need to think about it. The threading model is a programming convenience to simplify juggling several operations at the same time within a single program: The CPU will pop around and give each task some of its time.4 Each task has the consciousness of constantly having the CPU to itself, but the CPU’s time is being sliced among all the tasks (except when the program is actually running on multiple CPUs). One of the great things about threading is that you are abstracted away from this layer, so your code does not need to know whether it is running on a single CPU or many. Thus, using threads is a way to create transparently scalable programs—if a program is running too slowly, you can easily speed it up by adding CPUs to your computer. Multitasking and multithreading tend to be the most reasonable ways to utilize multiprocessor systems. Defining tasks A thread drives a task, so you need a way to describe that task. This is provided by the Runnable interface. To define a task, simply implement Runnable and write a run( ) method to make the task do your bidding. For example, the following LiftOff task displays the countdown before liftoff:
```java
//: concurrency/LiftOff.java
```

<!--p824-->
4 This is true when the system uses time slicing (Windows, for example). Solaris uses a FIFO concurrency model: Unless a higher-priority thread is awakened, the current thread runs until it blocks or terminates. That means that other threads with the same priority don’t run until the current one gives up the processor.
```java
// Demonstration of the Runnable interface.
public class LiftOff implements Runnable {
protected int countDown = 10; // Default
private static int taskCount = 0;
private final int id = taskCount++;
public LiftOff() {}
public LiftOff(int countDown) {
this.countDown = countDown;
}
public String status() {
return "#" + id + "(" +
(countDown > 0 ? countDown : "Liftoff!") + "), ";
}
public void run() {
while(countDown-- > 0) {
System.out.print(status());
Thread.yield();
}
}
} ///:~
```
The identifier id distinguishes between multiple instances of the task. It is final because it is not expected to change once it is initialized. A task’s run( ) method usually has some kind of loop that continues until the task is no longer necessary, so you must establish the condition on which to break out of this loop (one option is to simply return from run( )). Often, run( ) is cast in the form of an infinite loop, which means that, barring some factor that causes run( ) to terminate, it will continue forever (later in the chapter you’ll see how to safely terminate tasks). The call to the static method Thread.yield( ) inside run( ) is a suggestion to the thread scheduler (the part of the Java threading mechanism that moves the CPU from one thread to the next) that says, "I’ve done the important parts of my cycle and this would be a good time to switch to another task for a while." It’s completely optional, but it is used here because it tends to produce more interesting output in these examples: You’re more likely to see evidence of tasks being swapped in and out. In the following example, the task’s run( ) is not driven by a separate thread; it is simply called directly in main( ) (actually, this is using a thread: the one that is always allocated for main( )):
```java
//: concurrency/MainThread.java
public class MainThread {
public static void main(String[] args) {
LiftOff launch = new LiftOff();
launch.run();
}
} /* Output:
#0(9), #0(8), #0(7), #0(6), #0(5), #0(4), #0(3), #0(2), #0(1),
#0(Liftoff!),
*///:~
```
When a class is derived from Runnable, it must have a run( ) method, but that’s nothing special—it doesn’t produce any innate threading abilities. To achieve threading behavior, you must explicitly attach a task to a thread.
## The Thread class

<!--p825-->
Concurrency The traditional way to turn a Runnable object into a working task is to hand it to a Thread constructor. This example shows how to drive a Liftoff object using a Thread:
```java
//: concurrency/BasicThreads.java
// The most basic use of the Thread class.
public class BasicThreads {
public static void main(String[] args) {
Thread t = new Thread(new LiftOff());
t.start();
System.out.println("Waiting for LiftOff");
}
} /* Output: (90% match)
Waiting for LiftOff
#0(9), #0(8), #0(7), #0(6), #0(5), #0(4), #0(3), #0(2), #0(1),
#0(Liftoff!),
*///:~
```
A Thread constructor only needs a Runnable object. Calling a Thread object’s start( ) will perform the necessary initialization for the thread and then call that Runnable’s run( ) method to start the task in the new thread. Even though start( ) appears to be making a call to a long-running method, you can see from the output—the "Waiting for LiftOff’ message appears before the countdown has completed—that start( ) quickly returns. In effect, you have made a method call to LiftOff.run( ), and that method has not yet finished, but because LiftOff.run( ) is being executed by a different thread, you can still perform other operations in the main( ) thread. (This ability is not restricted to the main( ) thread—any thread can start another thread.) Thus, the program is running two methods at once— main( ) and LiftOff.run( ). run( ) is the code that is executed "simultaneously" with the other threads in a program. You can easily add more threads to drive more tasks. Here, you can see how all the tasks run in concert with one another:5
```java
//: concurrency/MoreBasicThreads.java
// Adding more threads.
public class MoreBasicThreads {
public static void main(String[] args) {
for(int i = 0; i < 5; i++)
new Thread(new LiftOff()).start();
System.out.println("Waiting for LiftOff");
}
} /* Output: (Sample)
Waiting for LiftOff
#0(9), #1(9), #2(9), #3(9), #4(9), #0(8), #1(8), #2(8), #3(8), #4(8),
#0(7), #1(7), #2(7), #3(7), #4(7), #0(6), #1(6), #2(6), #3(6), #4(6),
#0(5), #1(5), #2(5), #3(5), #4(5), #0(4), #1(4), #2(4), #3(4), #4(4),
#0(3), #1(3), #2(3), #3(3), #4(3), #0(2), #1(2), #2(2), #3(2), #4(2),
#0(1), #1(1), #2(1), #3(1), #4(1), #0(Liftoff!), #1(Liftoff!),
#2(Liftoff!), #3(Liftoff!), #4(Liftoff!),
*///:~
```

<!--p826-->
The output shows that the execution of the different tasks is mixed together as the threads are swapped in and out. This swapping is automatically controlled by the thread scheduler. If 5 In this case, a single thread (main( )), is creating all the LiftOff threads. If you have multiple threads creating LiftOff threads, however, it is possible for more than one LiftOff to have the same id. You’ll learn why later in this chapter. you have multiple processors on your machine, the thread scheduler will quietly distribute the threads among the processors.6 The output for one run of this program will be different from that of another, because the thread-scheduling mechanism is not deterministic. In fact, you may see dramatic differences in the output of this simple program between one version of the JDK and the next. For example, an earlier JDK didn’t timeslice very often, so thread l might loop to extinction first, then thread 2 would go through all of its loops, etc. This was virtually the same as calling a routine that would do all the loops at once, except that starting up all those threads is more expensive. Later JDKs seem to produce better time-slicing behavior, so each thread seems to get more regular service. Generally, these kinds of JDK behavioral changes have not been mentioned by Sun, so you cannot plan on any consistent threading behavior. The best approach is to be as conservative as possible while writing threaded code. When main( ) creates the Thread objects, it isn’t capturing the references for any of them. With an ordinary object, this would make it fair game for garbage collection, but not with a Thread. Each Thread "registers" itself so there is actually a reference to it someplace, and the garbage collector can’t clean it up until the task exits its run( ) and dies. You can see from the output that the tasks are indeed running to conclusion, so a thread creates a separate thread of execution that persists after the call to start( ) completes. Exercise 1:(2) Implement a Runnable. Inside run( ), print a message, and then call yield( ). Repeat this three times, and then return from run( ). Put a startup message in the constructor and a shutdown message when the task terminates. Create a number of these tasks and drive them using threads. Exercise 2:(2) Following the form of generics/Fibonacci.java, create a task that produces a sequence of n Fibonacci numbers, where n is provided to the constructor of the task. Create a number of these tasks and drive them using threads.
## Using Executors
Java SE5 java.util.concurrent Executors simplify concurrent programming by managing Thread objects for you. Executorsprovide a layer of indirection between a client and the execution of a task; instead of a client executing a task directly, an intermediate object executes the task. Executors allow you to manage the execution of asynchronous tasks without having to explicitly manage the lifecycle of threads. Executors are the preferred method for starting tasks in Java SE5/6. We can use an Executor instead of explicitly creating Thread objects in MoreBasicThreads.java. A LiftOff object knows how to run a specific task; like the Command design pattern, it exposes a single method to be executed. An ExecutorService (an Executor with a service lifecycle—e.g., shutdown) knows how to build the appropriate context to execute Runnable objects. In the following example, the CachedThreadPool creates one thread per task. Note that an ExecutorService object is created using a static Executors method which determines the kind of Executor it will be:
```java
//: concurrency/CachedThreadPool.java
import java.util.concurrent.*;
public class CachedThreadPool {
public static void main(String[] args) {
ExecutorService exec = Executors.newCachedThreadPool();
for(int i = 0; i < 5; i++)
exec.execute(new LiftOff());
```

<!--p827-->
6 This was not true for some of the earliest versions of Java.
```java
exec.shutdown();
}
} /* Output: (Sample)
#0(9), #0(8), #1(9), #2(9), #3(9), #4(9), #0(7), #1(8), #2(8), #3(8),
#4(8), #0(6), #1(7), #2(7), #3(7), #4(7), #0(5), #1(6), #2(6), #3(6),
#4(6), #0(4), #1(5), #2(5), #3(5), #4(5), #0(3), #1(4), #2(4), #3(4),
#4(4), #0(2), #1(3), #2(3), #3(3), #4(3), #0(1), #1(2), #2(2), #3(2),
#4(2), #0(Liftoff!), #1(1), #2(1), #3(1), #4(1), #1(Liftoff!),
#2(Liftoff!), #3(Liftoff!), #4(Liftoff!),
*///:~
```
Very often, a single Executor can be used to create and manage all the tasks in your system. The call to shutdown( ) prevents new tasks from being submitted to that Executor. The current thread (in this case, the one driving main( )) will continue to run all tasks submitted before shutdown( ) was called. The program will exit as soon as all the tasks in the Executor finish. You can easily replace the CachedThreadPool in the previous example with a different type of Executor. A FixedThreadPool uses a limited set of threads to execute the submitted tasks:
```java
//: concurrency/FixedThreadPool.java
import java.util.concurrent.*;
public class FixedThreadPool {
public static void main(String[] args) {
// Constructor argument is number of threads:
ExecutorService exec = Executors.newFixedThreadPool(5);
for(int i = 0; i < 5; i++)
exec.execute(new LiftOff());
exec.shutdown();
}
} /* Output: (Sample)
#0(9), #0(8), #1(9), #2(9), #3(9), #4(9), #0(7), #1(8), #2(8), #3(8),
#4(8), #0(6), #1(7), #2(7), #3(7), #4(7), #0(5), #1(6), #2(6), #3(6),
#4(6), #0(4), #1(5), #2(5), #3(5), #4(5), #0(3), #1(4), #2(4), #3(4),
#4(4), #0(2), #1(3), #2(3), #3(3), #4(3), #0(1), #1(2), #2(2), #3(2),
#4(2), #0(Liftoff!), #1(1), #2(1), #3(1), #4(1), #1(Liftoff!),
#2(Liftoff!), #3(Liftoff!), #4(Liftoff!),
*///:~
```

<!--p828-->
With the FixedThreadPool, you do expensive thread allocation once, up front, and you thus limit the number of threads. This saves time because you aren’t constantly paying for thread creation overhead for every single task. Also, in an event-driven system, event handlers that require threads can be serviced as quickly as you want by simply fetching threads from the pool. You don’t overrun the available resources because the FixedThreadPool uses a bounded number of Thread objects. Note that in any of the thread pools, existing threads are automatically reused when possible. Although this book will use CachedThreadPools, consider using FixedThreadPools in production code. A CachedThreadPool will generally create as many threads as it needs during the execution of a program and then will stop creating new threads as it recycles the old ones, so it’s a reasonable first choice as an Executor. Only if this approach causes problems do you need to switch to a FixedThreadPool. Concurrency A SingleThreadExecutor is like a FixedThreadPool with a size of one thread.7This is useful for anything you want to run in another thread continually (a long-lived task), such as a task that listens to incoming socket connections. It is also handy for short tasks that you want to run in a thread— for example, small tasks that update a local or remote log, or for an eventdispatching thread. If more than one task is submitted to a SingleThreadExecutor, the tasks will be queued and each task will run to completion before the next task is begun, all using the same thread. In the following example, you’ll see each task completed, in the order in which it was submitted, before the next one is begun. Thus, a SingleThreadExecutor serializes the tasks that are submitted to it, and maintains its own (hidden) queue of pending tasks.
```java
//: concurrency/SingleThreadExecutor.java
import java.util.concurrent.*;
public class SingleThreadExecutor {
public static void main(String[] args) {
ExecutorService exec =
Executors.newSingleThreadExecutor();
for(int i = 0; i < 5; i++)
exec.execute(new LiftOff());
exec.shutdown();
}
} /* Output:
#0(9), #0(8), #0(7), #0(6), #0(5), #0(4), #0(3), #0(2), #0(1),
#0(Liftoff!), #1(9), #1(8), #1(7), #1(6), #1(5), #1(4), #1(3), #1(2),
#1(1), #1(Liftoff!), #2(9), #2(8), #2(7), #2(6), #2(5), #2(4), #2(3),
#2(2), #2(1), #2(Liftoff!), #3(9), #3(8), #3(7), #3(6), #3(5), #3(4),
#3(3), #3(2), #3(1), #3(Liftoff!), #4(9), #4(8), #4(7), #4(6), #4(5),
#4(4), #4(3), #4(2), #4(1), #4(Liftoff!),
*///:~
```

<!--p829-->
As another example, suppose you have a number of threads running tasks that use the file system. You can run these tasks with a SingleThreadExecutor to ensure that only one task at a time is running from any thread. This way, you don’t need to deal with synchronizing on the shared resource (and you won’t clobber the file system in the meantime). Sometimes a better solution is to synchronize on the resource (which you’ll learn about later in this chapter), but a SingleThreadExecutor lets you skip the trouble of getting coordinated properly just to prototype something. By serializing tasks, you can eliminate the need to serialize the objects. Exercise 3: (1) Repeat Exercise 1 using the different types of executors shown in this section. Exercise 4: (1) Repeat Exercise 2 using the different types of executors shown in this section. Producing return values from tasks A Runnable is a separate task that performs work, but it doesn’t return a value. If you want the task to produce a value when it’s done, you can implement the Callable interface rather than the Runnable interface. Callable, introduced in Java SE5, is a generic with a type parameter representing the return value from the method call( ) (instead of run( )), and must be invoked using an ExecutorService submit( ) method. Here’s a simple example: 7 It also offers an important concurrency guarantee that the others do not—no two tasks will be called concurrently. This changes the locking requirements for the tasks (you’ll learn about locking later in the chapter).
```java
//: concurrency/CallableDemo.java
import java.util.concurrent.*;
import java.util.*;
class TaskWithResult implements Callable<String> {
private int id;
public TaskWithResult(int id) {
this.id = id;
}
public String call() {
return "result of TaskWithResult " + id;
}
}
public class CallableDemo {
public static void main(String[] args) {
ExecutorService exec = Executors.newCachedThreadPool();
ArrayList<Future<String>> results =
new ArrayList<Future<String>>();
for(int i = 0; i < 10; i++)
results.add(exec.submit(new TaskWithResult(i)));
for(Future<String> fs : results)
try {
// get() blocks until completion:
System.out.println(fs.get());
} catch(InterruptedException e) {
System.out.println(e);
return;
} catch(ExecutionException e) {
System.out.println(e);
} finally {
exec.shutdown();
}
}
} /* Output:
result of TaskWithResult 0
result of TaskWithResult 1
result of TaskWithResult 2
result of TaskWithResult 3
result of TaskWithResult 4
result of TaskWithResult 5
result of TaskWithResult 6
result of TaskWithResult 7
result of TaskWithResult 8
result of TaskWithResult 9
*///:~
```

<!--p830-->
The submit( ) method produces a Future object, parameterized for the particular type of result returned by the Callable. You can query the Future with isDone( ) to see if it has completed. When the task is completed and has a result, you can call get( ) to fetch the result. You can simply call get( ) without checking isDone( ), in which case get( ) will block until the result is ready. You can also call get( ) with a timeout, or isDone( ) to see if the task has completed, before trying to call get( ) to fetch the result. The overloaded Executors.callable( ) method takes a Runnable and produces a Callable. ExecutorService has some "invoke" methods that run collections of Callable objects. Exercise 5:(2) Modify Exercise 2 so that the task is a Callable that sums the values of all the Fibonacci numbers. Create several tasks and display the results. Concurrency Sleeping A simple way to affect the behavior of your tasks is by calling sleep( ) to cease (block) the execution of that task for a given time. In the LiftOff class, if you replace the call to yield( ) with a call to sleep( ), you get the following:
```java
//: concurrency/SleepingTask.java
// Calling sleep() to pause for a while.
import java.util.concurrent.*;
public class SleepingTask extends LiftOff {
public void run() {
try {
while(countDown-- > 0) {
System.out.print(status());
// Old-style:
// Thread.sleep(100);
// Java SE5/6-style:
TimeUnit.MILLISECONDS.sleep(100);
}
} catch(InterruptedException e) {
System.err.println("Interrupted");
}
}
public static void main(String[] args) {
ExecutorService exec = Executors.newCachedThreadPool();
for(int i = 0; i < 5; i++)
exec.execute(new SleepingTask());
exec.shutdown();
}
} /* Output:
#0(9), #1(9), #2(9), #3(9), #4(9), #0(8), #1(8), #2(8), #3(8), #4(8),
#0(7), #1(7), #2(7), #3(7), #4(7), #0(6), #1(6), #2(6), #3(6), #4(6),
#0(5), #1(5), #2(5), #3(5), #4(5), #0(4), #1(4), #2(4), #3(4), #4(4),
#0(3), #1(3), #2(3), #3(3), #4(3), #0(2), #1(2), #2(2), #3(2), #4(2),
#0(1), #1(1), #2(1), #3(1), #4(1), #0(Liftoff!), #1(Liftoff!),
#2(Liftoff!), #3(Liftoff!), #4(Liftoff!),
*///:~
```

<!--p831-->
The call to sleep( ) can throw an InterruptedException, and you can see that this is caught in run( ). Because exceptions won’t propagate across threads back to main( ), you must locally handle any exceptions that arise within a task. Java SE5 introduced the more explicit version of sleep( ) as part of the TimeUnit class, as shown in the above example. This provides better readability by allowing you to specify the units of the sleep( ) delay. TimeUnit can also be used to perform conversions, as you shall see later in the chapter. Depending on your platform, you may notice that the tasks run in "perfectly distributed" order—zero through four, then back to zero again. This makes sense because, after each print statement, each task goes to sleep (it blocks), which allows the thread scheduler to switch to another thread, driving another task. However, the sequential behavior relies on the underlying threading mechanism, which is different from one operating system to another, so you cannot rely on it. If you must control the order of execution of tasks, your best bet is to use synchronization controls (described later) or, in some cases, not to use threads at all, but instead to write your own cooperative routines that hand control to each other in a specified order. Exercise 6:(2) Create a task that sleeps for a random amount of time between 1 and 10 seconds, then displays its sleep time and exits. Create and run a quantity (given on the command line) of these tasks. Priority The priority of a thread conveys the importance of a thread to the scheduler. Although the order in which the CPU runs a set of threads is indeterminate, the scheduler will lean toward running the waiting thread with the highest priority first. However, this doesn’t mean that threads with lower priority aren’t run (so you can’t get deadlocked because of priorities). Lower-priority threads just tend to run less often. The vast majority of the time, all threads should run at the default priority. Trying to manipulate thread priorities is usually a mistake. Here’s an example that demonstrates priority levels. You can read the priority of an existing thread with getPriority( ) and change it at any time with setPriority( ).
```java
//: concurrency/SimplePriorities.java
// Shows the use of thread priorities.
import java.util.concurrent.*;
public class SimplePriorities implements Runnable {
private int countDown = 5;
private volatile double d; // No optimization
private int priority;
public SimplePriorities(int priority) {
this.priority = priority;
}
public String toString() {
return Thread.currentThread() + ": " + countDown;
}
public void run() {
Thread.currentThread().setPriority(priority);
while(true) {
// An expensive, interruptable operation:
for(int i = 1; i < 100000; i++) {
d += (Math.PI + Math.E) / (double)i;
if(i % 1000 == 0)
Thread.yield();
}
System.out.println(this);
if(--countDown == 0) return;
}
}
public static void main(String[] args) {
ExecutorService exec = Executors.newCachedThreadPool();
for(int i = 0; i < 5; i++)
exec.execute(
new SimplePriorities(Thread.MIN_PRIORITY));
exec.execute(
new SimplePriorities(Thread.MAX_PRIORITY));
exec.shutdown();
}
} /* Output: (70% match)
Thread[pool-1-thread-6,10,main]: 5
Thread[pool-1-thread-6,10,main]: 4
Thread[pool-1-thread-6,10,main]: 3
Thread[pool-1-thread-6,10,main]: 2
Thread[pool-1-thread-6,10,main]: 1
```

<!--p832-->
Concurrency
```java
Thread[pool-1-thread-3,1,main]: 5
Thread[pool-1-thread-2,1,main]: 5
Thread[pool-1-thread-1,1,main]: 5
Thread[pool-1-thread-5,1,main]: 5
Thread[pool-1-thread-4,1,main]: 5
...
*///:~
```

<!--p833-->
toString( ) is overridden to use Thread.toString( ), which prints the thread name, the priority level, and the "thread group" that the thread belongs to. You can set the thread name yourself via the constructor; here it’s automatically generated as pool-1-thread-1, pool-1- thread-2, etc. The overridden toString( ) also shows the countdown value of the task. Notice that you can get a reference to the Thread object that is driving a task, inside that task, by calling Thread.currentThread( ). You can see that the priority level of the last thread is at the highest level, and all the rest of the threads are at the lowest level. Note that the priority is set at the beginning of run( ); setting it in the constructor would do no good since the Executor has not begun the task at that point. Inside run( ), 100,000 repetitions of a rather expensive floating point calculation are performed, involving double addition and division. The variable d is volatile to try to ensure that no compiler optimizations are performed. Without this calculation, you don’t see the effect of setting the priority levels. (Try it: Comment out the for loop containing the double calculations.) With the calculation, you see that the thread with MAX_PRIORITY is given a higher preference by the thread scheduler. (At least, this was the behavior on a Windows XP machine.) Even though printing to the console is also an expensive behavior, you won’t see the priority levels that way, because console printing doesn’t get interrupted (otherwise, the console display would get garbled during threading), whereas the math calculation can be interrupted. The calculation takes long enough that the scheduling mechanism jumps in, swaps tasks, and pays attention to the priorities so that high-priority threads get preference. However, to ensure that a context switch occurs, yield( ) statements are regularly called. Although the JDK has 10 priority levels, this doesn’t map well to many operating systems. For example, Windows has 7 priority levels that are not fixed, so the mapping is indeterminate. Sun’s Solaris has 231 levels. The only portable approach is to stick to MAX_PRIORITY, NORM_PRIORITY, and MIN_PRIORITY when you’re adjusting priority levels. Yielding If you know that you’ve accomplished what you need to during one pass through a loop in your run( ) method, you can give a hint to the threadscheduling mechanism that you’ve done enough and that some other task might as well have the CPU. This hint (and it is a hint—there’s no guarantee your implementation will listen to it) takes the form of the yield( ) method. When you call yield( ), you are suggesting that other threads of the same priority might be run. LiftOff.java uses yield( ) to produce well-distributed processing across the various LiftOff tasks. Try commenting out the call to Thread.yield( ) in LiftOff.run( ) to see the difference. In general, however, you can’t rely on yield( ) for any serious control or tuning of your application. Indeed, yield( ) is often used incorrectly. Daemon threads A "daemon" thread is intended to provide a general service in the background as long as the program is running, but is not part of the essence of the program. Thus, when all of the non- daemon threads complete, the program is terminated, killing all daemon threads in the process. Conversely, if there are any non-daemon threads still running, the program doesn’t terminate. There is, for instance, a non-daemon thread that runs main( ).
```java
//: concurrency/SimpleDaemons.java
// Daemon threads don’t prevent the program from ending.
import java.util.concurrent.*;
import static net.mindview.util.Print.*;
public class SimpleDaemons implements Runnable {
public void run() {
try {
while(true) {
TimeUnit.MILLISECONDS.sleep(100);
print(Thread.currentThread() + " " + this);
}
} catch(InterruptedException e) {
print("sleep() interrupted");
}
}
public static void main(String[] args) throws Exception {
for(int i = 0; i < 10; i++) {
Thread daemon = new Thread(new SimpleDaemons());
daemon.setDaemon(true); // Must call before start()
daemon.start();
}
print("All daemons started");
TimeUnit.MILLISECONDS.sleep(175);
}
} /* Output: (Sample)
All daemons started
Thread[Thread-0,5,main] SimpleDaemons@530daa
Thread[Thread-1,5,main] SimpleDaemons@a62fc3
Thread[Thread-2,5,main] SimpleDaemons@89ae9e
Thread[Thread-3,5,main] SimpleDaemons@1270b73
Thread[Thread-4,5,main] SimpleDaemons@60aeb0
Thread[Thread-5,5,main] SimpleDaemons@16caf43
Thread[Thread-6,5,main] SimpleDaemons@66848c
Thread[Thread-7,5,main] SimpleDaemons@8813f2
Thread[Thread-8,5,main] SimpleDaemons@1d58aae
Thread[Thread-9,5,main] SimpleDaemons@83cc67
...
*///:~
```
You must set the thread to be a daemon by calling setDaemon( ) before it is started. There’s nothing to keep the program from terminating once main( ) finishes its job, since there are nothing but daemon threads running. So that you can see the results of starting all the daemon threads, the main( ) thread is briefly put to sleep. Without this, you see only some of the results from the creation of the daemon threads. (Try sleep( ) calls of various lengths to see this behavior.) SimpleDaemons.java creates explicit Thread objects in order to set their daemon flag. It is possible to customize the attributes (daemon, priority, name) of threads created by Executorsby writing a custom ThreadFactory:
```java
//: net/mindview/util/DaemonThreadFactory.java
package net.mindview.util;
import java.util.concurrent.*;
```

<!--p834-->
Concurrency
```java
public class DaemonThreadFactory implements ThreadFactory {
public Thread newThread(Runnable r) {
Thread t = new Thread(r);
t.setDaemon(true);
return t;
}
} ///:~
```
The only difference from an ordinary ThreadFactory is that this one sets the daemon status to true. You can now pass a new DaemonThreadFactory as an argument to Executors.newCachedThreadPool( ):
```java
//: concurrency/DaemonFromFactory.java
// Using a Thread Factory to create daemons.
import java.util.concurrent.*;
import net.mindview.util.*;
import static net.mindview.util.Print.*;
public class DaemonFromFactory implements Runnable {
public void run() {
try {
while(true) {
TimeUnit.MILLISECONDS.sleep(100);
print(Thread.currentThread() + " " + this);
}
} catch(InterruptedException e) {
print("Interrupted");
}
}
public static void main(String[] args) throws Exception {
ExecutorService exec = Executors.newCachedThreadPool(
new DaemonThreadFactory());
for(int i = 0; i < 10; i++)
exec.execute(new DaemonFromFactory());
print("All daemons started");
TimeUnit.MILLISECONDS.sleep(500); // Run for a while
}
} /* (Execute to see output) *///:~
```
Each of the static ExecutorService creation methods is overloaded to take a ThreadFactory object that it will use to create new threads. We can take this one step further and create a DaemonThreadPoolExecutor utility:
```java
//: net/mindview/util/DaemonThreadPoolExecutor.java
package net.mindview.util;
import java.util.concurrent.*;
public class DaemonThreadPoolExecutor
extends ThreadPoolExecutor {
public DaemonThreadPoolExecutor() {
super(0, Integer.MAX_VALUE, 60L, TimeUnit.SECONDS,
new SynchronousQueue<Runnable>(),
new DaemonThreadFactory());
}
} ///:~
```

<!--p835-->
To get the values for the constructor base-class call, I simply looked at the Executors.java source code. You can find out if a thread is a daemon by calling isDaemon( ). If a thread is a daemon, then any threads it creates will automatically be daemons, as the following example demonstrates:
```java
//: concurrency/Daemons.java
// Daemon threads spawn other daemon threads.
import java.util.concurrent.*;
import static net.mindview.util.Print.*;
class Daemon implements Runnable {
private Thread[] t = new Thread[10];
public void run() {
for(int i = 0; i < t.length; i++) {
t[i] = new Thread(new DaemonSpawn());
t[i].start();
printnb("DaemonSpawn " + i + " started, ");
}
for(int i = 0; i < t.length; i++)
printnb("t[" + i + "].isDaemon() = " +
t[i].isDaemon() + ", ");
while(true)
Thread.yield();
}
}
class DaemonSpawn implements Runnable {
public void run() {
while(true)
Thread.yield();
}
}
public class Daemons {
public static void main(String[] args) throws Exception {
Thread d = new Thread(new Daemon());
d.setDaemon(true);
d.start();
printnb("d.isDaemon() = " + d.isDaemon() + ", ");
// Allow the daemon threads to
// finish their startup processes:
TimeUnit.SECONDS.sleep(1);
}
} /* Output: (Sample)
d.isDaemon() = true, DaemonSpawn 0 started, DaemonSpawn 1 started,
DaemonSpawn 2 started, DaemonSpawn 3 started, DaemonSpawn 4 started,
DaemonSpawn 5 started, DaemonSpawn 6 started, DaemonSpawn 7 started,
DaemonSpawn 8 started, DaemonSpawn 9 started, t[0].isDaemon() = true,
t[1].isDaemon() = true, t[2].isDaemon() = true, t[3].isDaemon() = true,
t[4].isDaemon() = true, t[5].isDaemon() = true, t[6].isDaemon() = true,
t[7].isDaemon() = true, t[8].isDaemon() = true, t[9].isDaemon() = true,
*///:~
```
The Daemon thread is set to daemon mode. It then spawns a bunch of other threads—which are nor explicitly set to daemon mode—to show that they are daemons anyway. Then Daemon goes into an infinite loop that calls yield( ) to give up control to the other processes. You should be aware that daemon threads will terminate their run( ) methods without executing finally clauses:
```java
//: concurrency/DaemonsDontRunFinally.java
```

<!--p836-->
Concurrency
```java
// Daemon threads don’t run the finally clause
import java.util.concurrent.*;
import static net.mindview.util.Print.*;
class ADaemon implements Runnable {
public void run() {
try {
print("Starting ADaemon");
TimeUnit.SECONDS.sleep(1);
} catch(InterruptedException e) {
print("Exiting via InterruptedException");
} finally {
print("This should always run?");
}
}
}
public class DaemonsDontRunFinally {
public static void main(String[] args) throws Exception {
Thread t = new Thread(new ADaemon());
t.setDaemon(true);
t.start();
}
} /* Output:
Starting ADaemon
*///:~
```
When you run this program, you’ll see that the finally clause is not executed, but if you comment out the call to setDaemon( ), you’ll see that the finally clause is executed. This behavior is correct, even if you don’t expect it based on the previous promises given for finally. Daemons are terminated "abruptly" when the last of the non-daemons terminates. So as soon as main( ) exits, the JVM shuts down all the daemons immediately, without any of the formalities you might have come to expect. Because you cannot shut daemons down in a nice fashion, they are rarely a good idea. Non-daemon Executors are generally a better approach, since all the tasks controlled by an Executor can be shut down at once. As you shall see later in the chapter, shutdown in this case proceeds in an orderly fashion. Exercise 7: (2) Experiment with different sleep times in Daemons.java to see what happens. Exercise 8:(1) Modify MoreBasicThreads.java so that all the threads are daemon threads, and verify that the program ends as soon as main( ) is able to exit. Exercise 9:(3) Modify SimplePriorities.java so that a custom ThreadFactory sets the priorities of the threads. Coding variations In the examples that you’ve seen so far, the task classes all implement Runnable. In very simple cases, you may want to use the alternative approach of inheriting directly from Thread, like this:

<!--p837-->
```java
//: concurrency/SimpleThread.java
// Inheriting directly from the Thread class.
public class SimpleThread extends Thread {
private int countDown = 5;
private static int threadCount = 0;
public SimpleThread() {
// Store the thread name:
super(Integer.toString(++threadCount));
start();
}
public String toString() {
return "#" + getName() + "(" + countDown + "), ";
}
public void run() {
while(true) {
System.out.print(this);
if(--countDown == 0)
return;
}
}
public static void main(String[] args) {
for(int i = 0; i < 5; i++)
new SimpleThread();
}
} /* Output:
#1(5), #1(4), #1(3), #1(2), #1(1), #2(5), #2(4), #2(3), #2(2), #2(1),
#3(5), #3(4), #3(3), #3(2), #3(1), #4(5), #4(4), #4(3), #4(2), #4(1),
#5(5), #5(4), #5(3), #5(2), #5(1),
*///:~
```
You give the Thread objects specific names by calling the appropriate Thread constructor. This name is retrieved in toString( ) using getName( ). Another idiom that you may see is that of the self-managed Runnable:
```java
//: concurrency/SelfManaged.java
// A Runnable containing its own driver Thread.
public class SelfManaged implements Runnable {
private int countDown = 5;
private Thread t = new Thread(this);
public SelfManaged() { t.start(); }
public String toString() {
return Thread.currentThread().getName() +
"(" + countDown + "), ";
}
public void run() {
while(true) {
System.out.print(this);
if(--countDown == 0)
return;
}
}
public static void main(String[] args) {
for(int i = 0; i < 5; i++)
new SelfManaged();
}
} /* Output:
Thread-0(5), Thread-0(4), Thread-0(3), Thread-0(2), Thread-0(1), Thread-
1(5), Thread-1(4), Thread-1(3), Thread-1(2), Thread-1(1), Thread-2(5),
Thread-2(4), Thread-2(3), Thread-2(2), Thread-2(1), Thread-3(5), Thread-
3(4), Thread-3(3), Thread-3(2), Thread-3(1), Thread-4(5), Thread-4(4),
Thread-4(3), Thread-4(2), Thread-4(1),
*///:~
```

<!--p838-->
Concurrency This is not especially different from inheriting from Thread except that the syntax is slightly more awkward. However, implementing an interface does allow you to inherit from a different class, whereas inheriting from Thread does not. Notice that start( ) is called within the constructor. This example is quite simple and therefore probably safe, but you should be aware that starting threads inside a constructor can be quite problematic, because another task might start executing before the constructor has completed, which means the task may be able to access the object in an unstable state. This is yet another reason to prefer the use of Executorsto the explicit creation of Thread objects. Sometimes it makes sense to hide your threading code inside your class by using an inner class, as shown here:

<!--p839-->
```java
//: concurrency/ThreadVariations.java
// Creating threads with inner classes.
import java.util.concurrent.*;
import static net.mindview.util.Print.*;
// Using a named inner class:
class InnerThread1 {
private int countDown = 5;
private Inner inner;
private class Inner extends Thread {
Inner(String name) {
super(name);
start();
}
public void run() {
try {
while(true) {
print(this);
if(--countDown == 0) return;
sleep(10);
}
} catch(InterruptedException e) {
print("interrupted");
}
}
public String toString() {
return getName() + ": " + countDown;
}
}
public InnerThread1(String name) {
inner = new Inner(name);
}
}
// Using an anonymous inner class:
class InnerThread2 {
private int countDown = 5;
private Thread t;
public InnerThread2(String name) {
t = new Thread(name) {
public void run() {
try {
while(true) {
print(this);
if(--countDown == 0) return;
sleep(10);
}
} catch(InterruptedException e) {
print("sleep() interrupted");
}
}
public String toString() {
return getName() + ": " + countDown;
}
};
t.start();
}
}
// Using a named Runnable implementation:
class InnerRunnable1 {
private int countDown = 5;
private Inner inner;
private class Inner implements Runnable {
Thread t;
Inner(String name) {
t = new Thread(this, name);
t.start();
}
public void run() {
try {
while(true) {
print(this);
if(--countDown == 0) return;
TimeUnit.MILLISECONDS.sleep(10);
}
} catch(InterruptedException e) {
print("sleep() interrupted");
}
}
public String toString() {
return t.getName() + ": " + countDown;
}
}
public InnerRunnable1(String name) {
inner = new Inner(name);
}
}
// Using an anonymous Runnable implementation:
class InnerRunnable2 {
private int countDown = 5;
private Thread t;
public InnerRunnable2(String name) {
t = new Thread(new Runnable() {
public void run() {
try {
while(true) {
print(this);
if(--countDown == 0) return;
TimeUnit.MILLISECONDS.sleep(10);
}
} catch(InterruptedException e) {
print("sleep() interrupted");
}
}
public String toString() {
return Thread.currentThread().getName() +
": " + countDown;
}
}, name);
```

<!--p840-->
Concurrency
```java
t.start();
}
}
// A separate method to run some code as a task:
class ThreadMethod {
private int countDown = 5;
private Thread t;
private String name;
public ThreadMethod(String name) { this.name = name; }
public void runTask() {
if(t == null) {
t = new Thread(name) {
public void run() {
try {
while(true) {
print(this);
if(--countDown == 0) return;
sleep(10);
}
} catch(InterruptedException e) {
print("sleep() interrupted");
}
}
public String toString() {
return getName() + ": " + countDown;
}
};
t.start();
}
}
}
public class ThreadVariations {
public static void main(String[] args) {
new InnerThread1("InnerThread1");
new InnerThread2("InnerThread2");
new InnerRunnable1("InnerRunnable1");
new InnerRunnable2("InnerRunnable2");
new ThreadMethod("ThreadMethod").runTask();
}
} /* (Execute to see output) *///:~
```

<!--p841-->

<!--p842-->
InnerThread1 creates a named inner class that extends Thread, and makes an instance of this inner class inside the constructor. This makes sense if the inner class has special capabilities (new methods) that you need to access in other methods. However, most of the time the reason for creating a thread is only to use the Thread capabilities, so it’s not necessary to create a named inner class. InnerThread2 shows the alternative: An anonymous inner subclass of Thread is created inside the constructor and is upcast to a Thread reference t. If other methods of the class need to access t, they can do so through the Thread interface, and they don’t need to know the exact type of the object. The third and fourth classes in the example repeat the first two classes, but they use the Runnable interface rather than the Thread class. The ThreadMethod class shows the creation of a thread inside a method. You call the method when you’re ready to run the thread, and the method returns after the thread begins. If the thread is only performing an auxiliary operation rather than being fundamental to the class, this is probably a more useful and appropriate approach than starting a thread inside the constructor of the class. Exercise 10:(4) Modify Exercise 5 following the example of the ThreadMethod class, so that runTask( ) takes an argument of the number of Fibonacci numbers to sum, and each time you call runTask( ) it returns the Future produced by the call to submit( ). Terminology As the previous section shows, you have choices in how you implement concurrent programs in Java, and these choices can be confusing. Often the problem comes from the terminology that’s used in describing concurrent program technology, especially where threads are involved. You should see by now that there’s a distinction between the task that’s being executed and the thread that drives it; this distinction is especially clear in the Java libraries because you don’t really have any control over the Thread class (and this separation is even clearer with executors, which take care of the creation and management of threads for you). You create tasks and somehow attach a thread to your task so that the thread will drive that task. In Java, the Thread class by itself does nothing. It drives the task that it’s given. Yet threading literature invariably uses language like "the thread performs this or that action." The impression that you get is that the thread is the task, and when I first encountered Java threads, this impression was so strong that I saw a clear "is-a" relationship, which said to me that I should obviously inherit a task from a Thread. Add to this the poor choice of name for the Runnable interface, which I think would have been much better named "Task." If the interface is clearly nothing more than a generic encapsulation of its methods, then the "it- does-this-thing-able" naming approach is appropriate, but if it intends to express a higher concept, like Task, then the concept name is more helpful. The problem is that the levels of abstraction are mixed together. Conceptually, we want to create a task that runs independently of other tasks, so we ought to be able to define a task, and then say "go," and not worry about details. But physically, threads can be expensive to create, so you must conserve and manage them. Thus it makes sense from an implementation standpoint to separate tasks from threads. In addition, Java threading is based on the low-level pthreads approach which comes from C, where you are immersed in, and must thoroughly understand, the nuts and bolts of everything that’s going on. Some of this low-level nature has trickled through into the Java implementation, so to stay at a higher level of abstraction, you must use discipline when writing code (I will try to demonstrate that discipline in this chapter). To clarify these discussions, I shall attempt to use the term "task" when I am describing the work that is being done, and "thread" only when I am referring to the specific mechanism that’s driving the task. Thus, if you are discussing a system at a conceptual level, you could just use the term "task" without mentioning the driving mechanism at all. Joining a thread One thread may call join( ) on another thread to wait for the second thread to complete before proceeding. If a thread calls t.join( ) on another thread t, then the calling thread is suspended until the target thread t finishes (when t.isAlive( ) is false). You may also call join( ) with a timeout argument (in either milliseconds or milliseconds and nanoseconds) so that if the target thread doesn’t finish in that period of time, the call to join( ) returns anyway. The call to join( ) may be aborted by calling interrupt( ) on the calling thread, so a try- catch clause is required. Concurrency All of these operations are shown in the following example:
```java
//: concurrency/Joining.java
// Understanding join().
import static net.mindview.util.Print.*;
class Sleeper extends Thread {
private int duration;
public Sleeper(String name, int sleepTime) {
super(name);
duration = sleepTime;
start();
}
public void run() {
try {
sleep(duration);
} catch(InterruptedException e) {
print(getName() + " was interrupted. " +
"isInterrupted(): " + isInterrupted());
return;
}
print(getName() + " has awakened");
}
}
class Joiner extends Thread {
private Sleeper sleeper;
public Joiner(String name, Sleeper sleeper) {
super(name);
this.sleeper = sleeper;
start();
}
public void run() {
try {
sleeper.join();
} catch(InterruptedException e) {
print("Interrupted");
}
print(getName() + " join completed");
}
}
public class Joining {
public static void main(String[] args) {
Sleeper
sleepy = new Sleeper("Sleepy", 1500),
grumpy = new Sleeper("Grumpy", 1500);
Joiner
dopey = new Joiner("Dopey", sleepy),
doc = new Joiner("Doc", grumpy);
grumpy.interrupt();
}
} /* Output:
Grumpy was interrupted. isInterrupted(): false
Doc join completed
Sleepy has awakened
Dopey join completed
*///:~
```

<!--p843-->
A Sleeper is a thread that goes to sleep for a time specified in its constructor. In run( ), the call to sleep( ) may terminate when the time expires, but it may also be interrupted. Inside the catch clause, the interruption is reported, along with the value of isInterrupted( ). When another thread calls interrupt( ) on this thread, a flag is set to indicate that the thread has been interrupted. However, this flag is cleared when the exception is caught, so the result will always be false inside the catch clause. The flag is used for other situations where a thread may examine its interrupted state apart from the exception. A Joiner is a task that waits for a Sleeper to wake up by calling join( ) on the Sleeper object. In main( ), each Sleeper has a Joiner, and you can see in the output that if the Sleeper either is interrupted or ends normally, the Joiner completes in conjunction with the Sleeper. Note that the Java SE5 java.util.concurrent libraries contain tools such as CyclicBarrier (demonstrated later in this chapter) that may be more appropriate than join( ), which was part of the original threading library. Creating responsive user interfaces As stated earlier, one of the motivations for using threading is to create a responsive user interface. Although we won’t get to graphical interfaces until the Graphical User Interfaces chapter, the following example is a simple mock-up of a console-based user interface. The example has two versions: one that gets stuck in a calculation and thus can never read console input, and a second that puts the calculation inside a task and thus can be performing the calculation and listening for console input.
```java
//: concurrency/ResponsiveUI.java
// User interface responsiveness.
// {RunByHand}
class UnresponsiveUI {
private volatile double d = 1;
public UnresponsiveUI() throws Exception {
while(d > 0)
d = d + (Math.PI + Math.E) / d;
System.in.read(); // Never gets here
}
}
public class ResponsiveUI extends Thread {
private static volatile double d = 1;
public ResponsiveUI() {
setDaemon(true);
start();
}
public void run() {
while(true) {
d = d + (Math.PI + Math.E) / d;
}
}
public static void main(String[] args) throws Exception {
//! new UnresponsiveUI(); // Must kill this process
new ResponsiveUI();
System.in.read();
System.out.println(d); // Shows progress
}
} ///:~
```

<!--p844-->
UnresponsiveUI performs a calculation inside an infinite while loop, so it can obviously never reach the console input line (the compiler is fooled into believing that the input line is reachable by the while conditional). If you uncomment the line that creates an UnresponsiveUI, you’ll have to kill the process to get out. Concurrency To make the program responsive, put the calculation inside a run( ) method to allow it to be preempted, and when you press the Enter key, you’ll see that the calculation has indeed been running in the background while waiting for your user input. Thread groups A thread group holds a collection of threads. The value of thread groups can be summed up by a quote from Joshua Bloch,8the software architect who, while he was at Sun, fixed and greatly improved the Java collections library in JDK 1.2 (among other contributions): "Thread groups are best viewed as an unsuccessful experiment, and you may simply ignore their existence." If you’ve spent time and energy trying to figure out the value of thread groups (as I have), you may wonder why there was not some more official announcement from Sun on the topic—the same question can be asked about any number of other changes that have happened to Java over the years. The Nobel laureate economist Joseph Stiglitz has a philosophy of life that would seem to apply here.9It’s called The Theory of Escalating Commitment: "The cost of continuing mistakes is borne by others, while the cost of admitting mistakes is borne by yourself." Catching exceptions Because of the nature of threads, you can’t catch an exception that has escaped from a thread. Once an exception gets outside of a task’s run( ) method, it will propagate out to the console unless you take special steps to capture such errant exceptions. Before Java SE5, you used thread groups to catch these exceptions, but with Java SE5 you can solve the problem with Executors, and thus you no longer need to know anything about thread groups (except to understand legacy code; see Thinking in Java, 2ndEdition, downloadable from www.MindView.net, for details about thread groups). Here’s a task that always throws an exception which propagates outside of its run( ) method, and a main( ) that shows what happens when you run it:
```java
//: concurrency/ExceptionThread.java
// {ThrowsException}
import java.util.concurrent.*;
public class ExceptionThread implements Runnable {
public void run() {
throw new RuntimeException();
}
public static void main(String[] args) {
ExecutorService exec = Executors.newCachedThreadPool();
exec.execute(new ExceptionThread());
}
} ///:~
```
The output is (after trimming some qualifiers to fit):
```java
java.lang.RuntimeException
```

<!--p845-->
8Effective Java™ Programming Language Guide, by Joshua Bloch (Addison-Wesley, 2001), p. 211. 9 And in a number of other places throughout the experience of Java. Well, why stop there? I’ve consulted on more than a few projects where this has applied.
```java
at ExceptionThread.run(ExceptionThread.java:7)
at ThreadPoolExecutor$Worker.runTask(Unknown Source)
at ThreadPoolExecutor$Worker.run(Unknown Source)
at Java.lang.Thread.run(Unknown Source)
```
Encompassing the body of main within a try-catch block is unsuccessful:
```java
//: concurrency/NaiveExceptionHandling.java
// {ThrowsException}
import java.util.concurrent.*;
public class NaiveExceptionHandling {
public static void main(String[] args) {
try {
ExecutorService exec =
Executors.newCachedThreadPool();
exec.execute(new ExceptionThread());
} catch(RuntimeException ue) {
// This statement will NOT execute!
System.out.println("Exception has been handled!");
}
}
} ///:~
```
This produces the same result as the previous example: an uncaught exception. To solve the problem, we change the way the Executor produces threads. Thread.UncaughtExceptionHandler is a new interface in Java SE5; it allows you to attach an exception handler to each Thread object. Thread.UncaughtExceptionHandler.uncaughtException( ) is automatically called when that thread is about to die from an uncaught exception. To use it, we create a new type of ThreadFactory which attaches a new Thread.UncaughtExceptionHandler to each new Thread object it creates. We pass that factory to the Executors method that creates a new ExecutorService:
```java
//: concurrency/CaptureUncaughtException.java
import java.util.concurrent.*;
class ExceptionThread2 implements Runnable {
public void run() {
Thread t = Thread.currentThread();
System.out.println("run() by " + t);
System.out.println(
"eh = " + t.getUncaughtExceptionHandler());
throw new RuntimeException();
}
}
class MyUncaughtExceptionHandler implements
Thread.UncaughtExceptionHandler {
public void uncaughtException(Thread t, Throwable e) {
System.out.println("caught " + e);
}
}
class HandlerThreadFactory implements ThreadFactory {
public Thread newThread(Runnable r) {
System.out.println(this + " creating new Thread");
Thread t = new Thread(r);
System.out.println("created " + t);
t.setUncaughtExceptionHandler(
```

<!--p846-->
Concurrency
```java
new MyUncaughtExceptionHandler());
System.out.println(
"eh = " + t.getUncaughtExceptionHandler());
return t;
}
}
public class CaptureUncaughtException {
public static void main(String[] args) {
ExecutorService exec = Executors.newCachedThreadPool(
new HandlerThreadFactory());
exec.execute(new ExceptionThread2());
}
} /* Output: (90% match)
HandlerThreadFactory@de6ced creating new Thread
created Thread[Thread-0,5,main]
eh = MyUncaughtExceptionHandler@1fb8ee3
run() by Thread[Thread-0,5,main]
eh = MyUncaughtExceptionHandler@1fb8ee3
caught java.lang.RuntimeException
*///:~
```
Additional tracing has been added to verify that the threads created by the factory are given the new UncaughtExceptionHandler. You can see that the uncaught exceptions are now being captured by uncaughtException. The above example allows you to set the handler on a case-by-case basis. If you know that you’re going to use the same exception handler everywhere, an even simpler approach is to set the default uncaught exception handler, which sets a static field inside the Thread class:
```java
//: concurrency/SettingDefaultHandler.java
import java.util.concurrent.*;
public class SettingDefaultHandler {
public static void main(String[] args) {
Thread.setDefaultUncaughtExceptionHandler(
new MyUncaughtExceptionHandler());
ExecutorService exec = Executors.newCachedThreadPool();
exec.execute(new ExceptionThread());
}
} /* Output:
caught java.lang.RuntimeException
*///:~
```

<!--p847-->
This handler is only called if there is no per-thread uncaught exception handler. The system checks for a per-thread version, and if it doesn’t find one it checks to see if the thread group specializes its uncaughtException( ) method; if not, it calls the defaultUncaughtExceptionHandler. Sharing resources You can think of a single-threaded program as one lonely entity moving around through your problem space and doing one thing at a time. Because there’s only one entity, you never have to think about the problem of two entities trying to use the same resource at the same time: problems such as two people trying to park in the same space, walk through a door at the same time, or even talk at the same time. With concurrency, things aren’t lonely anymore, but you now have the possibility of two or more tasks interfering with each other. If you don’t prevent such a collision, you’ll have two tasks trying to access the same bank account at the same time, print to the same printer, adjust the same valve, and so on. Improperly accessing resources Consider the following example, where one task generates even numbers and other tasks consume those numbers. Here, the only job of the consumer tasks is to check the validity of the even numbers. First we’ll define EvenChecker, the consumer task, since it will be reused in all the subsequent examples. To decouple EvenChecker from the various types of generators that we will experiment with, we’ll create an abstract class called IntGenerator, which contains the minimum necessary methods that EvenChecker must know about: that it has a next( ) method and that it can be canceled. This class doesn’t implement the Generator interface, because it must produce an int, and generics don’t support primitive parameters.
```java
//: concurrency/IntGenerator.java
public abstract class IntGenerator {
private volatile boolean canceled = false;
public abstract int next();
// Allow this to be canceled:
public void cancel() { canceled = true; }
public boolean isCanceled() { return canceled; }
} ///:~
```
IntGenerator has a cancel( ) method to change the state of a boolean canceled flag and isCanceled( ) to see whether the object has been canceled. Because the canceled flag is a boolean, it is atomic, which means that simple operations like assignment and value return happen without the possibility of interruption, so you can’t see the field in an intermediate state in the midst of those simple operations. The canceled flag is also volatile in order to ensure visibility. You’ll learn about atomicity and visibility later in this chapter. Any IntGenerator can be tested with the following EvenChecker class:
```java
//: concurrency/EvenChecker.java
import java.util.concurrent.*;
public class EvenChecker implements Runnable {
private IntGenerator generator;
private final int id;
public EvenChecker(IntGenerator g, int ident) {
generator = g;
id = ident;
}
public void run() {
while(!generator.isCanceled()) {
int val = generator.next();
if(val % 2 != 0) {
System.out.println(val + " not even!");
generator.cancel(); // Cancels all EvenCheckers
}
}
}
// Test any type of IntGenerator:
public static void test(IntGenerator gp, int count) {
System.out.println("Press Control-C to exit");
ExecutorService exec = Executors.newCachedThreadPool();
for(int i = 0; i < count; i++)
```

<!--p848-->
Concurrency
```java
exec.execute(new EvenChecker(gp, i));
exec.shutdown();
}
// Default value for count:
public static void test(IntGenerator gp) {
test(gp, 10);
}
} ///:~
```
Note that in this example the class that can be canceled is not Runnable. Instead, all the EvenChecker tasks that depend on the IntGenerator object test it to see whether it’s been canceled, as you can see in run( ). This way, the tasks that share the common resource (the IntGenerator) watch that resource for the signal to terminate. This eliminates the so-called race condition, where two or more tasks race to respond to a condition and thus collide or otherwise produce inconsistent results. You must be careful to think about and protect against all the possible ways a concurrent system can fail. For example, a task cannot depend on another task, because task shutdown order is not guaranteed. Here, by making tasks depend on a nontask object, we eliminate the potential race condition. The test( ) method sets up and performs a test of any type of IntGenerator by starting a number of EvenCheckers that use the same IntGenerator. Ifthe IntGenerator causes a failure, test( ) will report it and return; otherwise, you must press Control-C to terminate it. EvenChecker tasks constantly read and test the values from their associated IntGenerator. Note that if generator.isCanceled( ) is true, run( ) returns, which tells the Executor in EvenChecker.test( ) that the task is complete. Any EvenChecker task can call cancel( ) on its associated IntGenerator, which will cause all other EvenCheckers using that IntGenerator to gracefully shut down. In later sections, you’ll see that Java contains more general mechanisms for termination of threads. The first IntGenerator we’ll look at has a next( ) that produces a series of even values:
```java
//: concurrency/EvenGenerator.java
// When threads collide.
public class EvenGenerator extends IntGenerator {
private int currentEvenValue = 0;
public int next() {
++currentEvenValue; // Danger point here!
++currentEvenValue;
return currentEvenValue;
}
public static void main(String[] args) {
EvenChecker.test(new EvenGenerator());
}
} /* Output: (Sample)
Press Control-C to exit
89476993 not even!
89476993 not even!
*///:~
```

<!--p849-->

<!--p850-->
It’s possible for one task to call next( ) after another task has performed the first increment of currentEvenValue but not the second (at the place in the code commented "Danger point here!"). This puts the value into an "incorrect" state. To prove that this can happen, EvenChecker.test( ) creates a group of EvenChecker objects to continually read the output of an EvenGenerator and test to see if each one is even. If not, the error is reported and the program is shut down. This program will eventually fail because the EvenChecker tasks are able to access the information in EvenGenerator while it’s in an "incorrect" state. However, it may not detect the problem until the EvenGenerator has completed many cycles, depending on the particulars of your operating system and other implementation details. If you want to see it fail much faster, try putting a call to yield( ) between the first and second increments. This is part of the problem with multithreaded programs—they can appear to be correct even when there’s a bug, if the probability for failure is very low. It’s important to note that the increment operation itself requires multiple steps, and the task can be suspended by the threading mechanism in the midst of an increment—that is, increment is not an atomic operation in Java. So even a single increment isn’t safe to do without protecting the task. Resolving shared resource contention The previous example shows a fundamental problem when you are using threads: You never know when a thread might be run. Imagine sitting at a table with a fork, about to spear the last piece of food on a platter, and as your fork reaches for it, the food suddenly vanishes— because your thread was suspended and another diner came in and ate the food. That’s the problem you’re dealing with when writing concurrent programs. For concurrency to work, you need some way to prevent two tasks from accessing the same resource, at least during critical periods. Preventing this kind of collision is simply a matter of putting a lock on a resource when one task is using it. The first task that accesses a resource must lock it, and then the other tasks cannot access that resource until it is unlocked, at which time another task locks and uses it, and so on. If the front seat of the car is the limited resource, the child who shouts "shotgun!" acquires the lock (for the duration of that trip). To solve the problem of thread collision, virtually all concurrency schemes serialize access to shared resources. This means that only one task at a time is allowed to access the shared resource. This is ordinarily accomplished by putting a clause around a piece of code that only allows one task at a time to pass through that piece of code. Because this clause produces mutual exclusion, a common name for such a mechanism is mutex. Consider the bathroom in your house; multiple people (tasks driven by threads) may each want to have exclusive use of the bathroom (the shared resource). To access the bathroom, a person knocks on the door to see if it’s available. If so, they enter and lock the door. Any other task that wants to use the bathroom is "blocked" from using it, so those tasks wait at the door until the bathroom is available. The analogy breaks down a bit when the bathroom is released and it comes time to give access to another task. There isn’t actually a line of people, and we don’t know for sure who gets the bathroom next, because the thread scheduler isn’t deterministic that way. Instead, it’s as if there is a group of blocked tasks milling about in front of the bathroom, and when the task that has locked the bathroom unlocks it and emerges, the one that happens to be nearest the door at the moment goes in. As noted earlier, suggestions can be made to the thread scheduler via yield( ) and setPriority( ), but these suggestions may not have much of an effect, depending on your platform and JVM implementation. To prevent collisions over resources, Java has built-in support in the form of the synchronized keyword. When a task wishes to execute a piece of code guarded by the synchronized keyword, it checks to see if the lock is available, then acquires it, executes the code, and releases it. The shared resource is typically just a piece of memory in the form of an object, but may also be a file, an I/O port, or something like a printer. To control access to a shared resource, you first put it inside an object. Then any method that uses the resource can be made synchronized. If a task is in a call to one of the synchronized methods, all other tasks are Concurrency blocked from entering any of the synchronized methods of that object until the first task returns from its call. In production code, you’ve already seen that you should make the data elements of a class private and access that memory only through methods. You can prevent collisions by declaring those methods synchronized, like this:
```java
synchronized void f() { /* ... */ }
synchronized void g() { /* ... */ }
```
All objects automatically contain a single lock (also referred to as a monitor). When you call any synchronized method, that object is locked and no other synchronized method of that object can be called until the first one finishes and releases the lock. For the preceding methods, if f( ) is called for an object by one task, a different task cannot call f( ) or g( ) for the same object until f( ) is completed and releases the lock. Thus, there is a single lock that is shared by all the synchronized methods of a particular object, and this lock can be used to prevent object memory from being written by more than one task at a time. Note that it’s especially important to make fields private when working with concurrency; otherwise the synchronized keyword cannot prevent another task from accessing a field directly, and thus producing collisions. One task may acquire an object’s lock multiple times. This happens if one method calls a second method on the same object, which in turn calls another method on the same object, etc. The JVM keeps track of the number of times the object has been locked. If the object is unlocked, it has a count of zero. As a task acquires the lock for the first time, the count goes to one. Each time the same task acquires another lock on the same object, the count is incremented. Naturally, multiple lock acquisition is only allowed for the task that acquired the lock in the first place. Each time the task leaves a synchronized method, the count is decremented, until the count goes to zero, releasing the lock entirely for use by other tasks. There’s also a single lock per class (as part of the Class object for the class), so that synchronized static methods can lock each other out from simultaneous access of static data on a class-wide basis. When should you synchronize? Apply Brian’s Rule of Synchronization:10 If you are writing a variable that might next be read by another thread, or reading a variable that might have last been written by another thread, you must use synchronization, and further, both the reader and the writer must synchronize using the same monitor lock. If you have more than one method in your class that deals with the critical data, you must synchronize all relevant methods. If you synchronize only one of the methods, then the others are free to ignore the object lock and can be called with impunity. This is an important point: Every method that accesses a critical shared resource must be synchronized or it won’t work right.
## Synchronizing the EvenGenerator
By adding synchronized to EvenGenerator.java, we can prevent the undesirable thread access:
```java
//: concurrency/SynchronizedEvenGenerator.java
```

<!--p851-->
10 From Brian Goetz, author of Java Concurrency in Practice, by Brian Goetz, Tim Peierls, Joshua Bloch, Joseph Bowbeer, David Holmes, and Doug Lea (Addison-Wesley, 2006).
```java
// Simplifying mutexes with the synchronized keyword.
// {RunByHand}
public class
SynchronizedEvenGenerator extends IntGenerator {
private int currentEvenValue = 0;
public synchronized int next() {
++currentEvenValue;
Thread.yield(); // Cause failure faster
++currentEvenValue;
return currentEvenValue;
}
public static void main(String[] args) {
EvenChecker.test(new SynchronizedEvenGenerator());
}
} ///:~
```
A call to Thread.yield( ) is inserted between the two increments, to raise the likelihood of a context switch while currentEvenValue is in an odd state. Because the mutex prevents more than one task at a time in the critical section, this will not produce a failure, but calling yield( ) is a helpful way to promote a failure if it’s going to happen. The first task that enters next( ) acquires the lock, and any further tasks that try to acquire the lock are blocked from doing so until the first task releases the lock. At that point, the scheduling mechanism selects another task that is waiting on the lock. This way, only one task at a time can pass through the code that is guarded by the mutex. Exercise 11:(3) Create a class containing two data fields, and a method that manipulates those fields in a multistep process so that, during the execution of that method, those fields are in an "improper state" (according to some definition that you establish). Add methods to read the fields, and create multiple threads to call the various methods and show that the data is visible in its "improper state." Fix the problem using the synchronized keyword.
## Using explicit Lock objects
The Java SE5 java.util.concurrent library also contains an explicit mutex mechanism defined in java.util.concurrent.locks. The Lock object must be explicitly created, locked and unlocked; thus, it produces less elegant code than the built-in form. However, it is more flexible for solving certain types of problems. Here is SynchronizedEvenGenerator.java rewritten to use explicit Locks:
```java
//: concurrency/MutexEvenGenerator.java
// Preventing thread collisions with mutexes.
// {RunByHand}
import java.util.concurrent.locks.*;
public class MutexEvenGenerator extends IntGenerator {
private int currentEvenValue = 0;
private Lock lock = new ReentrantLock();
public int next() {
lock.lock();
try {
++currentEvenValue;
Thread.yield(); // Cause failure faster
++currentEvenValue;
return currentEvenValue;
} finally {
lock.unlock();
}
}
```

<!--p852-->
Concurrency
```java
public static void main(String[] args) {
EvenChecker.test(new MutexEvenGenerator());
}
} ///:~
```
MutexEvenGenerator adds a mutex called lock and uses the lock( ) and unlock( ) methods to create a critical section within next( ). When you are using Lock objects, it is important to internalize the idiom shown here: Right after the call to lock( ), you must place a try-finally statement with unlock( ) in the finally clause—this is the only way to guarantee that the lock is always released. Note that the return statement must occur inside the try clause to ensure that the unlock( ) doesn’t happen too early and expose the data to a second task. Although the try-finally requires more code than using the synchronized keyword, it also represents one of the advantages of explicit Lock objects. If something fails using the synchronized keyword, an exception is thrown, but you don’t get the chance to do any cleanup in order to maintain your system in a good state. With explicit Lock objects, you can maintain proper state in your system using the finally clause. In general, when you are using synchronized, there is less code to write, and the opportunity for user error is greatly reduced, so you’ll usually only use the explicit Lock objects when you’re solving special problems. For example, with the synchronized keyword, you can’t try and fail to acquire a lock, or try to acquire a lock for a certain amount of time and then give up—to do this, you must use the concurrent library:

<!--p853-->
```java
//: concurrency/AttemptLocking.java
// Locks in the concurrent library allow you
// to give up on trying to acquire a lock.
import java.util.concurrent.*;
import java.util.concurrent.locks.*;
public class AttemptLocking {
private ReentrantLock lock = new ReentrantLock();
public void untimed() {
boolean captured = lock.tryLock();
try {
System.out.println("tryLock(): " + captured);
} finally {
if(captured)
lock.unlock();
}
}
public void timed() {
boolean captured = false;
try {
captured = lock.tryLock(2, TimeUnit.SECONDS);
} catch(InterruptedException e) {
throw new RuntimeException(e);
}
try {
System.out.println("tryLock(2, TimeUnit.SECONDS): " +
captured);
} finally {
if(captured)
lock.unlock();
}
}
public static void main(String[] args) {
final AttemptLocking al = new AttemptLocking();
al.untimed(); // True -- lock is available
al.timed(); // True -- lock is available
```
Concurrency
```java
// Now create a separate task to grab the lock:
new Thread() {
{ setDaemon(true); }
public void run() {
al.lock.lock();
System.out.println("acquired");
}
}.start();
Thread.yield(); // Give the 2nd task a chance
al.untimed(); // False -- lock grabbed by task
al.timed(); // False -- lock grabbed by task
}
} /* Output:
tryLock(): true
tryLock(2, TimeUnit.SECONDS): true
acquired
tryLock(): false
tryLock(2, TimeUnit.SECONDS): false
*///:~
```

<!--p854-->

<!--p855-->
A ReentrantLock allows you to try and fail to acquire the lock, so that if someone else already has the lock, you can decide to go off and do something else rather than waiting until it is free, as you can see in the untimed( ) method. In timed( ), an attempt is made to acquire the lock which can fail after 2 seconds (note the use of the Java SE5 TimeUnit class to specify units). In main( ), a separate Thread is created as an anonymous class, and it acquires the lock so that the untimed( ) and timed( ) methods have something to contend with. The explicit Lock object also gives you finer-grained control over locking and unlocking than does the built-in synchronized lock. This is useful for implementing specialized synchronization structures, such as hand-overhand locking (also called lock coupling), used for traversing the nodes of a linked list—the traversal code must capture the lock of the next node before it releases the current node’s lock. Atomicity and volatility An incorrect piece of lore that is often repeated in Java threading discussions is, "Atomic operations do not need to be synchronized." An atomic operation is one that cannot be interrupted by the thread scheduler; if the operation begins, then it will run to completion before the possibility of a context switch. Relying on atomicity is tricky and dangerous—you should only try to use atomicity instead of synchronization if you are a concurrency expert, or you have help from such an expert. If you think you’re smart enough to play with this kind of fire, take this test: The Goetz Test11: If you can write a high-performance JVM for a modern microprocessor, then you are qualified to think about whether you can avoid synchronizing.12 It’s useful to know about atomicity, and to know that, along with other advanced techniques, it was used to implement some of the more clever java.util.concurrent library components. But strongly resist the urge to rely on it yourself; see Brian’s Rule of Synchronization, presented earlier. 11 After the previously mentioned Brian Goetz, a concurrency expert who helped with this chapter, based on only partially tongue-in-cheek comments from him. 12 A corollary to this test is, "If someone implies that threading is easy and straightforward, make sure that person is not making important decisions about your project. If that person already is, then you’ve got trouble." Atomicity applies to "simple operations" on primitive types except for longs and doubles. Reading and writing primitive variables other than long and double is guaranteed to go to and from memory as indivisible (atomic) operations. However, the JVM is allowed to perform reads and writes of 64- bit quantities (long and double variables) as two separate 32-bit operations, raising the possibility that a context switch could happen in the middle of a read or write, and then different tasks could see incorrect results (this is sometimes called word tearing, because you might see the value after only part of it has been changed). However, you do get atomicity (for simple assignments and returns) if you use the volatile keyword when defining a long or double variable (note that volatile was not working properly before Java SE5). Different JVMs are free to provide stronger guarantees, but you should not rely on platform-specific features. Atomic operations are thus not interruptible by the threading mechanism. Expert programmers can take advantage of this to write lock-free code, which does not need to be synchronized. But even this is an oversimplification. Sometimes, even when it seems like an atomic operation should be safe, it may not be. Readers of this book will typically not be able to pass the aforementioned Goetz Test, and will thus not be qualified to try to replace synchronization with atomic operations. Trying to remove synchronization is usually a sign of premature optimization, and will cause you a lot of trouble, probably without gaining much, or anything. On multiprocessor systems (which are now appearing in the form of multicore processors— multiple CPUs on a single chip), visibility rather than atomicity is much more of an issue than on single-processor systems. Changes made by one task, even if they’re atomic in the sense of not being interruptible, might not be visible to other tasks (the changes might be temporarily stored in a local processor cache, for example), so different tasks will have a different view of the application’s state. The synchronization mechanism, on the other hand, forces changes by one task on a multiprocessor system to be visible across the application. Without synchronization, it’s indeterminate when changes become visible. The volatile keyword also ensures visibility across the application. If you declare a field to be volatile, this means that as soon as a write occurs for that field, all reads will see the change. This is true even if local caches are involved—volatile fields are immediately written through to main memory, and reads occur from main memory. It’s important to understand that atomicity and volatility are distinct concepts. An atomic operation on a non-volatile field will not necessarily be flushed to main memory, and so another task that reads that field will not necessarily see the new value. If multiple tasks are accessing a field, that field should be volatile; otherwise, the field should only be accessed via synchronization. Synchronization also causes flushing to main memory, so if a field is completely guarded by synchronized methods or blocks, it is not necessary to make it volatile. Any writes that a task makes will be visible to that task, so you don’t need to make a field volatile if it is only seen within a task. volatile doesn’t work when the value of a field depends on its previous value (such as incrementing a counter), nor does it work on fields whose values are constrained by the values of other fields, such as the lower and upper bound of a Range class which must obey the constraint lower <= upper. It’s typically only safe to use volatile instead of synchronized if the class has only one mutable field. Again, your first choice should be to use the synchronized keyword—that’s the safest approach, and trying to do anything else is risky. What qualifies as an atomic operation? Assignment and returning the value in a field will usually be atomic. However, in C++ even the following might be atomic: Concurrency
```java
i++; // Might be atomic in C++
i +=2; // Might be atomic in C++
```
But in C++, this depends on the compiler and processor. You’re unable to write cross- platform code in C++ that relies on atomicity, because C++ doesn’t have a consistent memory model, as Java does (in Java SEs).13 In Java, the above operations are definitely not atomic, as you can see from the JVM instructions produced by the following methods:
```java
//: concurrency/Atomicity.java
// {Exec: javap -c Atomicity}
public class Atomicity {
int i;
void f1() { i++; }
void f2() { i += 3; }
} /* Output: (Sample)
...
void f1();
Code:
0: aload_0
1: dup
2: getfield #2; //Field i:I
5: iconst_1
6: iadd
7: putfield #2; //Field i:I
10: return
void f2();
Code:
0: aload_0
1: dup
2: getfield #2; //Field i:I
5: iconst_3
6: iadd
7: putfield #2; //Field i:I
10: return
*///:~
```
Each instruction produces a "get" and a "put," with instructions in between. So in between getting and putting, another task could modify the field, and thus the operations are not atomic. If you blindly apply the idea of atomicity, you see that getValue( ) in the following program fits the description:
```java
//: concurrency/AtomicityTest.java
import java.util.concurrent.*;
public class AtomicityTest implements Runnable {
private int i = 0;
public int getValue() { return i; }
private synchronized void evenIncrement() { i++; i++; }
public void run() {
while(true)
evenIncrement();
}
```

<!--p856-->
13 This is being remedied in the upcoming C++ standard.
```java
public static void main(String[] args) {
ExecutorService exec = Executors.newCachedThreadPool();
AtomicityTest at = new AtomicityTest();
exec.execute(at);
while(true) {
int val = at.getValue();
if(val % 2 != 0) {
System.out.println(val);
System.exit(0);
}
}
}
} /* Output: (Sample)
191583767
*///:~
```
However, the program will find non-even values and terminate. Although return i is indeed an atomic operation, the lack of synchronization allows the value to be read while the object is in an unstable intermediate state. On top of this, since i is also not volatile, there will be visibility problems. Both getValue( ) and evenIncrement( ) must be synchronized. Only concurrency experts are qualified to attempt optimizations in situations like this; again, you should apply Brian’s Rule of Synchronization. As a second example, consider something even simpler: a class that produces serial numbers.14 Each time nextSerialNumber( ) is called, it must return a unique value to the caller:
```java
//: concurrency/SerialNumberGenerator.java
public class SerialNumberGenerator {
private static volatile int serialNumber = 0;
public static int nextSerialNumber() {
return serialNumber++; // Not thread-safe
}
} ///:~
```

<!--p857-->
SerialNumberGenerator is about as simple a class as you can imagine, and if you’re coming from C++ or some other low-level background, you might expect the increment to be an atomic operation, because a C++ increment can often be implemented as a microprocessor instruction (although not in any reliable, cross-platform fashion). As noted before, however, a Java increment is not atomic and involves both a read and a write, so there’s room for threading problems even in such a simple operation. As you shall see, volatility isn’t actually the issue here; the real problem is that nextSerialNumber( ) accesses a shared, mutable value without synchronizing. The serialNumber field is volatile because it is possible for each thread to have a local stack and maintain copies of some variables there. If you define a variable as volatile, it tells the compiler not to do any optimizations that would remove reads and writes that keep the field in exact synchronization with the local data in the threads. In effect, reads and writes go directly to memory, and are not cached, volatile also restricts compiler reordering of accesses during optimization. However, volatile doesn’t affect the fact that an increment isn’t an atomic operation. Basically, you should make a field volatile if that field could be simultaneously accessed by multiple tasks, and at least one of those accesses is a write. For example, a field that is used as a flag to stop a task must be declared volatile; otherwise, that flag could be cached in a 14 Inspired by Joshua Bloch’s Effective Java™ Programming Language Guide (Addison- Wesley, 2001), p. 190. register, and when you make changes to the flag from outside the task, the cached value wouldn’t be changed and the task wouldn’t know it should stop. To test SerialNumberGenerator, we need a set that doesn’t run out of memory, in case it takes a long time to detect a problem. The CircularSet shown here reuses the memory used to store ints, with the assumption that by the time you wrap around, the possibility of a collision with the overwritten values is minimal. The add( ) and contains( ) methods are synchronized to prevent thread collisions:
```java
//: concurrency/SerialNumberChecker.java
// Operations that may seem safe are not,
// when threads are present.
// {Args: 4}
import java.util.concurrent.*;
// Reuses storage so we don’t run out of memory:
class CircularSet {
private int[] array;
private int len;
private int index = 0;
public CircularSet(int size) {
array = new int[size];
len = size;
// Initialize to a value not produced
// by the SerialNumberGenerator:
for(int i = 0; i < size; i++)
array[i] = -1;
}
public synchronized void add(int i) {
array[index] = i;
// Wrap index and write over old elements:
index = ++index % len;
}
public synchronized boolean contains(int val) {
for(int i = 0; i < len; i++)
if(array[i] == val) return true;
return false;
}
}
public class SerialNumberChecker {
private static final int SIZE = 10;
private static CircularSet serials =
new CircularSet(1000);
private static ExecutorService exec =
Executors.newCachedThreadPool();
static class SerialChecker implements Runnable {
public void run() {
while(true) {
int serial =
SerialNumberGenerator.nextSerialNumber();
if(serials.contains(serial)) {
System.out.println("Duplicate: " + serial);
System.exit(0);
}
serials.add(serial);
}
}
}
public static void main(String[] args) throws Exception {
for(int i = 0; i < SIZE; i++)
exec.execute(new SerialChecker());
```

<!--p858-->
Concurrency
```java
// Stop after n seconds if there’s an argument:
if(args.length > 0) {
TimeUnit.SECONDS.sleep(new Integer(args[0]));
System.out.println("No duplicates detected");
System.exit(0);
}
}
} /* Output: (Sample)
Duplicate: 8468656
*///:~
```
SerialNumberChecker contains a static CircularSet that holds all the serial numbers that have been produced, and a nested SerialChecker class that ensures the serial numbers are unique. By creating multiple tasks to contend over serial numbers, you’ll discover that the tasks eventually get a duplicate serial number, if you let it run long enough. To solve the problem, add the synchronized keyword to nextSerialNumber( ). The atomic operations that are supposed to be safe are the reading and assignment of primitives. However, as seen in AtomicityTest.java, it’s still easily possible to use an atomic operation that accesses your object while it’s in an unstable intermediate state. Making assumptions about this issue is tricky and dangerous. The most sensible thing to do is just to follow Brian’s Rule of Synchronization. Exercise 12:(3) Repair AtomicityTest.java using the synchronized keyword. Can you demonstrate that it is now correct? Exercise 13:(1) Repair SerialNumberChecker.java using the synchronized keyword. Can you demonstrate that it is now correct? Atomic classes Java SE5 introduces special atomic variable classes such as Atomiclnteger, AtomicLong, AtomicReference, etc. that provide an atomic conditional update operation of the form:
```java
boolean compareAndSet(expectedValue, updateValue);
```
These are for fine-tuning to use machine-level atomicity that is available on some modern processors, so you generally don’t need to worry about using them. Occasionally they come in handy for regular coding, but again when performance tuning is involved. For example, we can rewrite AtomicityTest.java to use Atomiclnteger:

<!--p859-->
```java
//: concurrency/AtomicIntegerTest.java
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import java.util.*;
public class AtomicIntegerTest implements Runnable {
private AtomicInteger i = new AtomicInteger(0);
public int getValue() { return i.get(); }
private void evenIncrement() { i.addAndGet(2); }
public void run() {
while(true)
evenIncrement();
}
public static void main(String[] args) {
new Timer().schedule(new TimerTask() {
public void run() {
System.err.println("Aborting");
System.exit(0);
}
}, 5000); // Terminate after 5 seconds
ExecutorService exec = Executors.newCachedThreadPool();
AtomicIntegerTest ait = new AtomicIntegerTest();
exec.execute(ait);
while(true) {
int val = ait.getValue();
if(val % 2 != 0) {
System.out.println(val);
System.exit(0);
}
}
}
} ///:~
```
Here we’ve eliminated the synchronized keyword by using AtomicInteger instead. Because the program doesn’t fail, a Timer is added to automatically abort after 5 seconds. Here is MutexEvenGenerator.java rewritten to use Atomiclnteger:
```java
//: concurrency/AtomicEvenGenerator.java
// Atomic classes are occasionally useful in regular code.
// {RunByHand}
import java.util.concurrent.atomic.*;
public class AtomicEvenGenerator extends IntGenerator {
private AtomicInteger currentEvenValue =
new AtomicInteger(0);
public int next() {
return currentEvenValue.addAndGet(2);
}
public static void main(String[] args) {
EvenChecker.test(new AtomicEvenGenerator());
}
} ///:~
```
Again, all other forms of synchronization have been eliminated by using AtomicInteger. It should be emphasized that the Atomic classes were designed to build the classes in java.util.concurrent, and that you should use them in your own code only under special circumstances, and even then only when you can ensure that there are no other possible problems. It’s generally safer to rely on locks (either the synchronized keyword or explicit Lock objects). Exercise 14:(4) Demonstrate that java.util.Timer scales to large numbers by creating a program that generates many Timer objects that perform some simple task when the timeout completes. Critical sections Sometimes, you only want to prevent multiple thread access to part of the code inside a method instead of the entire method. The section of code you want to isolate this way is called a critical section and is created using the synchronized keyword. Here, synchronized is used to specify the object whose lock is being used to synchronize the enclosed code:
```java
synchronized(syncObject) {
// This code can be accessed
```

<!--p860-->
Concurrency
```java
// by only one task at a time
}
```
This is also called a synchronized block; before it can be entered, the lock must be acquired on syncObject. If some other task already has this lock, then the critical section cannot be entered until the lock is released. The following example compares both synchronization approaches by showing how the time available for other tasks to access an object is significantly increased by using a synchronized block instead of synchronizing an entire method. In addition, it shows how an unprotected class can be used in a multithreaded situation if it is controlled and protected by another class:

<!--p861-->
```java
//: concurrency/CriticalSection.java
// Synchronizing blocks instead of entire methods. Also
// demonstrates protection of a non-thread-safe class
// with a thread-safe one.
package concurrency;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import java.util.*;
class Pair { // Not thread-safe
private int x, y;
public Pair(int x, int y) {
this.x = x;
this.y = y;
}
public Pair() { this(0, 0); }
public int getX() { return x; }
public int getY() { return y; }
public void incrementX() { x++; }
public void incrementY() { y++; }
public String toString() {
return "x: " + x + ", y: " + y;
}
public class PairValuesNotEqualException
extends RuntimeException {
public PairValuesNotEqualException() {
super("Pair values not equal: " + Pair.this);
}
}
// Arbitrary invariant -- both variables must be equal:
public void checkState() {
if(x != y)
throw new PairValuesNotEqualException();
}
}
// Protect a Pair inside a thread-safe class:
abstract class PairManager {
AtomicInteger checkCounter = new AtomicInteger(0);
protected Pair p = new Pair();
private List<Pair> storage =
Collections.synchronizedList(new ArrayList<Pair>());
public synchronized Pair getPair() {
// Make a copy to keep the original safe:
return new Pair(p.getX(), p.getY());
}
// Assume this is a time consuming operation
protected void store(Pair p) {
storage.add(p);
try {
TimeUnit.MILLISECONDS.sleep(50);
} catch(InterruptedException ignore) {}
}
public abstract void increment();
}
// Synchronize the entire method:
class PairManager1 extends PairManager {
public synchronized void increment() {
p.incrementX();
p.incrementY();
store(getPair());
}
}
// Use a critical section:
class PairManager2 extends PairManager {
public void increment() {
Pair temp;
synchronized(this) {
p.incrementX();
p.incrementY();
temp = getPair();
}
store(temp);
}
}
class PairManipulator implements Runnable {
private PairManager pm;
public PairManipulator(PairManager pm) {
this.pm = pm;
}
public void run() {
while(true)
pm.increment();
}
public String toString() {
return "Pair: " + pm.getPair() +
" checkCounter = " + pm.checkCounter.get();
}
}
class PairChecker implements Runnable {
private PairManager pm;
public PairChecker(PairManager pm) {
this.pm = pm;
}
public void run() {
while(true) {
pm.checkCounter.incrementAndGet();
pm.getPair().checkState();
}
}
}
public class CriticalSection {
// Test the two different approaches:
static void
testApproaches(PairManager pman1, PairManager pman2) {
ExecutorService exec = Executors.newCachedThreadPool();
PairManipulator
pm1 = new PairManipulator(pman1),
pm2 = new PairManipulator(pman2);
```

<!--p862-->
Concurrency
```java
PairChecker
pcheck1 = new PairChecker(pman1),
pcheck2 = new PairChecker(pman2);
exec.execute(pm1);
exec.execute(pm2);
exec.execute(pcheck1);
exec.execute(pcheck2);
try {
TimeUnit.MILLISECONDS.sleep(500);
} catch(InterruptedException e) {
System.out.println("Sleep interrupted");
}
System.out.println("pm1: " + pm1 + "\npm2: " + pm2);
System.exit(0);
}
public static void main(String[] args) {
PairManager
pman1 = new PairManager1(),
pman2 = new PairManager2();
testApproaches(pman1, pman2);
}
} /* Output: (Sample)
pm1: Pair: x: 15, y: 15 checkCounter = 272565
pm2: Pair: x: 16, y: 16 checkCounter = 3956974
*///:~
```

<!--p863-->
As noted, Pair is not thread-safe because its invariant (admittedly arbitrary) requires that both variables maintain the same values. In addition, as seen earlier in this chapter, the increment operations are not thread-safe, and because none of the methods are synchronized, you can’t trust a Pair object to stay uncorrupted in a threaded program. You can imagine that someone hands you the non-thread-safe Pair class, and you need to use it in a threaded environment. You do this by creating the PairManager class, which holds a Pair object and controls all access to it. Note that the only public methods are getPair( ), which is synchronized, and the abstract increment( ). Synchronization for increment( ) will be handled when it is implemented. The structure of PairManager, where functionality implemented in the base class uses one or more abstract methods defined in derived classes, is called a Template Method in Design Patterns parlance.15 Design patterns allow you to encapsulate change in your code; here, the part that is changing is the method increment( ). In PairManager1 the entire increment( ) method is synchronized, but in PairManager2 only part of increment( ) is synchronized by using a synchronized block. Note that the synchronized keyword is not part of the method signature and thus may be added during overriding. The store( ) method adds a Pair object to a synchronized ArrayList, so this operation is thread safe. Thus, it doesn’t need to be guarded, and is placed outside of the synchronized block in PairManager2. PairManipulator is created to test the two different types of PairManagersby calling increment( ) in a task while a PairChecker is run from another task. To trace how often it is able to run the test, PairChecker increments checkCounter every time it is successful. In main( ), two PairManipulator objects are created and allowed to run for a while, after which the results of each PairManipulator are shown. Although you will probably see a lot of variation in output from one run to the next, in general you will see that PairManager1.increment( ) does not allow the PairChecker 15 See Design Patterns, by Gamma et al. (Addison-Wesley, 1995). nearly as much access as PairManager2.increment( ), which has the synchronized block and thus provides more unlocked time. This is typically the reason to use a synchronized block instead of synchronizing the whole method: to allow other tasks more access (as long as it is safe to do so). You can also use explicit Lock objects to create critical sections:
```java
//: concurrency/ExplicitCriticalSection.java
// Using explicit Lock objects to create critical sections.
package concurrency;
import java.util.concurrent.locks.*;
// Synchronize the entire method:
class ExplicitPairManager1 extends PairManager {
private Lock lock = new ReentrantLock();
public synchronized void increment() {
lock.lock();
try {
p.incrementX();
p.incrementY();
store(getPair());
} finally {
lock.unlock();
}
}
}
// Use a critical section:
class ExplicitPairManager2 extends PairManager {
private Lock lock = new ReentrantLock();
public void increment() {
Pair temp;
lock.lock();
try {
p.incrementX();
p.incrementY();
temp = getPair();
} finally {
lock.unlock();
}
store(temp);
}
}
public class ExplicitCriticalSection {
public static void main(String[] args) throws Exception {
PairManager
pman1 = new ExplicitPairManager1(),
pman2 = new ExplicitPairManager2();
CriticalSection.testApproaches(pman1, pman2);
}
} /* Output: (Sample)
pm1: Pair: x: 15, y: 15 checkCounter = 174035
pm2: Pair: x: 16, y: 16 checkCounter = 2608588
*///:~
```

<!--p864-->
This reuses most of CriticalSection.java and creates new PairManager types that use explicit Lock objects. ExplicitPairManager2 shows the creation of a critical section using a Lock object; the call to store( ) is outside of the critical section. Synchronizing on other objects Concurrency A synchronized block must be given an object to synchronize upon, and usually the most sensible object to use is just the current object that the method is being called for: synchronized(this), which is the approach taken in PairManager2. That way, when the lock is acquired for the synchronized block, other synchronized methods and critical sections in the object cannot be called. So the effect of the critical section, when synchronizing on this, is simply to reduce the scope of synchronization. Sometimes you must synchronize on another object, but if you do this you must ensure that all relevant tasks are synchronizing on the same object. The following example demonstrates that two tasks can enter an object when the methods in that object synchronize on different locks:
```java
//: concurrency/SyncObject.java
// Synchronizing on another object.
import static net.mindview.util.Print.*;
class DualSynch {
private Object syncObject = new Object();
public synchronized void f() {
for(int i = 0; i < 5; i++) {
print("f()");
Thread.yield();
}
}
public void g() {
synchronized(syncObject) {
for(int i = 0; i < 5; i++) {
print("g()");
Thread.yield();
}
}
}
}
public class SyncObject {
public static void main(String[] args) {
final DualSynch ds = new DualSynch();
new Thread() {
public void run() {
ds.f();
}
}.start();
ds.g();
}
} /* Output: (Sample)
g()
f()
g()
f()
g()
f()
g()
f()
g()
f()
*///:~
```

<!--p865-->
DualSync.f( ) synchronizes on this (by synchronizing the entire method), and g( ) has a synchronized block that synchronizes on syncObject. Thus, the two synchronizations are independent. This is demonstrated in main( ) by creating a Thread that calls f( ). The main( ) thread is used to call g( ). You can see from the output that both methods are running at the same time, so neither one is blocked by the synchronization of the other. Exercise 15: (1) Create a class with three methods containing critical sections that all synchronize on the same object. Create multiple tasks to demonstrate that only one of these methods can run at a time. Now modify the methods so that each one synchronizes on a different object and show that all three methods can be running at once. Exercise 16:(1) Modify Exercise 15 to use explicit Lock objects. Thread local storage A second way to prevent tasks from colliding over shared resources is to eliminate the sharing of variables. Thread local storage is a mechanism that automatically creates different storage for the same variable, for each different thread that uses an object. Thus, if you have five threads using an object with a variable x, thread local storage generates five different pieces of storage for x. Basically, they allow you to associate state with a thread. The creation and management of thread local storage is taken care of by the java.lang.ThreadLocal class, as seen here:
```java
//: concurrency/ThreadLocalVariableHolder.java
// Automatically giving each thread its own storage.
import java.util.concurrent.*;
import java.util.*;
class Accessor implements Runnable {
private final int id;
public Accessor(int idn) { id = idn; }
public void run() {
while(!Thread.currentThread().isInterrupted()) {
ThreadLocalVariableHolder.increment();
System.out.println(this);
Thread.yield();
}
}
public String toString() {
return "#" + id + ": " +
ThreadLocalVariableHolder.get();
}
}
public class ThreadLocalVariableHolder {
private static ThreadLocal<Integer> value =
new ThreadLocal<Integer>() {
private Random rand = new Random(47);
protected synchronized Integer initialValue() {
return rand.nextInt(10000);
}
};
public static void increment() {
value.set(value.get() + 1);
}
public static int get() { return value.get(); }
public static void main(String[] args) throws Exception {
ExecutorService exec = Executors.newCachedThreadPool();
for(int i = 0; i < 5; i++)
exec.execute(new Accessor(i));
TimeUnit.SECONDS.sleep(3); // Run for a while
exec.shutdownNow(); // All Accessors will quit
}
} /* Output: (Sample)
#0: 9259
```

<!--p866-->
Concurrency
```java
#1: 556
#2: 6694
#3: 1862
#4: 962
#0: 9260
#1: 557
#2: 6695
#3: 1863
#4: 963
...
*///:~
```
ThreadLocal objects are usually stored as static fields. When you create a ThreadLocal object, you are only able to access the contents of the object using the get( ) and set( ) methods. The get( ) method returns a copy of the object that is associated with that thread, and set( ) inserts its argument into the object stored for that thread, returning the old object that was in storage. The increment( ) and get( ) methods demonstrate this in ThreadLocalVariableHolder. Notice that increment( ) and get( ) are not synchronized, because ThreadLocal guarantees that no race condition can occur. When you run this program, you’ll see evidence that the individual threads are each allocated their own storage, since each one keeps its own count even though there’s only one ThreadLocalVariableHolder object. Terminating tasks In some of the previous examples, cancel( ) and isCanceled( ) methods are placed in a class that is seen by all tasks. The tasks check isCanceled( ) to determine when to terminate themselves. This is a reasonable approach to the problem. However, in some situations the task must be terminated more abruptly. In this section, you’ll learn about the issues and problems of such termination. First, let’s look at an example that not only demonstrates the termination problem but also is an additional example of resource sharing. The ornamental garden In this simulation, the garden committee would like to know how many people enter the garden each day through its multiple gates. Each gate has a turnstile or some other kind of counter, and after the turnstile count is incremented, a shared count is incremented that represents the total number of people in the garden.

<!--p867-->
```java
//: concurrency/OrnamentalGarden.java
import java.util.concurrent.*;
import java.util.*;
import static net.mindview.util.Print.*;
class Count {
private int count = 0;
private Random rand = new Random(47);
// Remove the synchronized keyword to see counting fail:
public synchronized int increment() {
int temp = count;
if(rand.nextBoolean()) // Yield half the time
Thread.yield();
return (count = ++temp);
}
public synchronized int value() { return count; }
}
class Entrance implements Runnable {
private static Count count = new Count();
private static List<Entrance> entrances =
new ArrayList<Entrance>();
private int number = 0;
// Doesn’t need synchronization to read:
private final int id;
private static volatile boolean canceled = false;
// Atomic operation on a volatile field:
public static void cancel() { canceled = true; }
public Entrance(int id) {
this.id = id;
// Keep this task in a list. Also prevents
// garbage collection of dead tasks:
entrances.add(this);
}
public void run() {
while(!canceled) {
synchronized(this) {
++number;
}
print(this + " Total: " + count.increment());
try {
TimeUnit.MILLISECONDS.sleep(100);
} catch(InterruptedException e) {
print("sleep interrupted");
}
}
print("Stopping " + this);
}
public synchronized int getValue() { return number; }
public String toString() {
return "Entrance " + id + ": " + getValue();
}
public static int getTotalCount() {
return count.value();
}
public static int sumEntrances() {
int sum = 0;
for(Entrance entrance : entrances)
sum += entrance.getValue();
return sum;
}
}
public class OrnamentalGarden {
public static void main(String[] args) throws Exception {
ExecutorService exec = Executors.newCachedThreadPool();
for(int i = 0; i < 5; i++)
exec.execute(new Entrance(i));
// Run for a while, then stop and collect the data:
TimeUnit.SECONDS.sleep(3);
Entrance.cancel();
exec.shutdown();
if(!exec.awaitTermination(250, TimeUnit.MILLISECONDS))
print("Some tasks were not terminated!");
print("Total: " + Entrance.getTotalCount());
print("Sum of Entrances: " + Entrance.sumEntrances());
}
} /* Output: (Sample)
```

<!--p868-->
Concurrency
```java
Entrance 0: 1 Total: 1
Entrance 2: 1 Total: 3
Entrance 1: 1 Total: 2
Entrance 4: 1 Total: 5
Entrance 3: 1 Total: 4
Entrance 2: 2 Total: 6
Entrance 4: 2 Total: 7
Entrance 0: 2 Total: 8
...
Entrance 3: 29 Total: 143
Entrance 0: 29 Total: 144
Entrance 4: 29 Total: 145
Entrance 2: 30 Total: 147
Entrance 1: 30 Total: 146
Entrance 0: 30 Total: 149
Entrance 3: 30 Total: 148
Entrance 4: 30 Total: 150
Stopping Entrance 2: 30
Stopping Entrance 1: 30
Stopping Entrance 0: 30
Stopping Entrance 3: 30
Stopping Entrance 4: 30
Total: 150
Sum of Entrances: 150
*///:~
```

<!--p869-->

<!--p870-->
A single Count object keeps the master count of garden visitors, and is stored as a static field in the Entrance class. Count.increment( ) and Count.value( ) are synchronized to control access to the count field. The increment( ) method uses a Random object to cause a yield( ) roughly half the time, in between fetching count into temp and incrementing and storing temp back into count. If you comment out the synchronized keyword on increment( ), the program breaks because multiple tasks will be accessing and modifying count simultaneously (the yield( ) causes the problem to happen more quickly). Each Entrance task keeps a local value number containing the number of visitors that have passed through that particular entrance. This provides a double check against the count object to make sure that the proper number of visitors is being recorded. Entrance.run( ) simply increments number and the count object and sleeps for 100 milliseconds. Because Entrance.canceled is a volatile boolean flag which is only read and assigned (and is never read in combination with other fields), it’s possible to get away without synchronizing access to it. If you have any doubts about something like this, it’s always better to use synchronized. This program goes to quite a bit of extra trouble to shut everything down in a stable fashion. Part of the reason for this is to show just how careful you must be when terminating a multithreaded program, and part of the reason is to demonstrate the value of interrupt( ), which you will learn about shortly. After 3 seconds, main( ) sends the static cancel( ) message to Entrance, then calls shutdown( ) for the exec object, and then calls awaitTermination( ) on exec. ExecutorService.awaitTermination( ) waits for each task to complete, and if they all complete before the timeout value, it returns true, otherwise it returns false to indicate that not all tasks have completed. Although this causes each task to exit its run( ) method and therefore terminate as a task, the Entrance objects are still valid because, in the constructor, each Entrance object is stored in a static List<Entrance> called entrances. Thus, sumEntrances( ) is still working with valid Entrance objects. As this program runs, you will see the total count and the count at each entrance displayed as people walk through a turnstile. If you remove the synchronized declaration on Count.increment( ), you’ll notice that the total number of people is not what you expect it to be. The number of people counted by each turnstile will be different from the value in count. As long as the mutex is there to synchronize access to the Count, things work correctly. Keep in mind that Count.increment( ) exaggerates the potential for failure by using temp and yield( ). In real threading problems, the possibility for failure may be statistically small, so you can easily fall into the trap of believing that things are working correctly. Just as in the example above, there are likely to be hidden problems that haven’t occurred to you, so be exceptionally diligent when reviewing concurrent code. Exercise 17:(2) Create a radiation counter that can have any number of remote sensors. Terminating when blocked Entrance.run( ) in the previous example includes a call to sleep( ) in its loop. We know that sleep( ) will eventually wake up and the task will reach the top of the loop, where it has an opportunity to break out of that loop by checking the cancelled flag. However, sleep( ) is just one situation where a task is blocked from executing, and sometimes you must terminate a task that’s blocked. Thread states A thread can be in any one of four states: 1.New: A thread remains in this state only momentarily, as it is being created. It allocates any necessary system resources and performs initialization. At this point it becomes eligible to receive CPU time. The scheduler will then transition this thread to the runnable or blocked state. 2.Runnable: This means that a thread can be run when the time-slicing mechanism has CPU cycles available for the thread. Thus, the thread might or might not be running at any moment, but there’s nothing to prevent it from being run if the scheduler can arrange it. That is, it’s not dead or blocked. 3.Blocked: The thread can be run, but something prevents it. While a thread is in the blocked state, the scheduler will simply skip it and not give it any CPU time. Until a thread reenters the runnable state, it won’t perform any operations. 4.Dead: A thread in the dead or terminated state is no longer schedulable and will not receive any CPU time. Its task is completed, and it is no longer runnable. One way for a task to die is by returning from its run( ) method, but a task’s thread can also be interrupted, as you’ll see shortly. Becoming blocked A task can become blocked for the following reasons: • You’ve put the task to sleep by calling sleep(milliseconds), in which case it will not be run for the specified time. • You’ve suspended the execution of the thread with wait( ). It will not become runnable again until the thread gets the notify( ) or notifyAll( ) message (or the equivalent signal( ) or signalAll( ) for the Java SE5 java.util.concurrent library tools). We’ll examine these in a later section. Concurrency • The task is waiting for some I/O to complete. • The task is trying to call a synchronized method on another object, and that object’s lock is not available because it has already been acquired by another task. In old code, you may also see suspend( ) and resume( ) used to block and unblock threads, but these are deprecated in modern Java (because they are deadlock-prone), and so will not be examined in this book. The stop( ) method is also deprecated, because it doesn’t release the locks that the thread has acquired, and if the objects are in an inconsistent state ("damaged"), other tasks can view and modify them in that state. The resulting problems can be subtle and difficult to detect. The problem we need to look at now is this: Sometimes you want to terminate a task that is in a blocked state. If you can’t wait for it to get to a point in the code where it can check a state value and decide to terminate on its own, you have to force the task out of its blocked state. Interruption As you might imagine, it’s much messier to break out of the middle of a Runnable.run( ) method than it is to wait for that method to get to a test of a "cancel" flag, or to some other place where the programmer is ready to leave the method. When you break out of a blocked task, you might need to clean up resources. Because of this, breaking out of the middle of a task’s run( ) is more like throwing an exception than anything else, so in Java threads, exceptions are used for this kind of abort.16(This walks the fine edge of being an inappropriate use of exceptions, because it means you are often using them for control flow.) To return to a known good state when terminating a task this way, you must carefully consider the execution paths of your code and write your catch clause to properly clean everything up. So that you can terminate a blocked task, the Thread class contains the interrupt( ) method. This sets the interrupted status for that thread. A thread with its interrupted status set will throw an InterruptedException if it is already blocked or if it attempts a blocking operation. The interrupted status will be reset when the exception is thrown or if the task calls Thread.interrupted( ). As you’ll see, Thread.interrupted( ) provides a second way to leave your run( ) loop, without throwing an exception. To call interrupt( ), you must hold a Thread object. You may have noticed that the new concurrent library seems to avoid the direct manipulation of Thread objects and instead tries to do everything through Executors. If you call shutdownNow( ) on an Executor, it will send an interrupt( ) call to each of the threads it has started. This makes sense because you’ll usually want to shut down all the tasks for a particular Executor at once, when you’ve finished part of a project or a whole program. However, there are times when you may want to only interrupt a single task. If you’re using Executors, you can hold on to the context of a task when you start it by calling submit( ) instead of execute( ). submit( ) returns a generic Future<?>, with an unspecified parameter because you won’t ever call get( ) on it— the point of holding this kind of Future is that you can call cancel( ) on it and thus use it to interrupt a particular task. If you pass true to cancel( ), it has permission to call interrupt( ) on that thread in order to stop it; thus cancel( ) is a way to interrupt individual threads started with an Executor. Here’s an example that shows the basics of interrupt( ) using Executors:
```java
//: concurrency/Interrupting.java
```

<!--p871-->
16 However, exceptions are never delivered asynchronously. Thus, there is no danger of something aborting mid- instruction/method call. And as long as you use the try-finally idiom when using object mutexes (vs. the synchronized keyword), those mutexes will be automatically released if an exception is thrown.
```java
// Interrupting a blocked thread.
import java.util.concurrent.*;
import java.io.*;
import static net.mindview.util.Print.*;
class SleepBlocked implements Runnable {
public void run() {
try {
TimeUnit.SECONDS.sleep(100);
} catch(InterruptedException e) {
print("InterruptedException");
}
print("Exiting SleepBlocked.run()");
}
}
class IOBlocked implements Runnable {
private InputStream in;
public IOBlocked(InputStream is) { in = is; }
public void run() {
try {
print("Waiting for read():");
in.read();
} catch(IOException e) {
if(Thread.currentThread().isInterrupted()) {
print("Interrupted from blocked I/O");
} else {
throw new RuntimeException(e);
}
}
print("Exiting IOBlocked.run()");
}
}
class SynchronizedBlocked implements Runnable {
public synchronized void f() {
while(true) // Never releases lock
Thread.yield();
}
public SynchronizedBlocked() {
new Thread() {
public void run() {
f(); // Lock acquired by this thread
}
}.start();
}
public void run() {
print("Trying to call f()");
f();
print("Exiting SynchronizedBlocked.run()");
}
}
public class Interrupting {
private static ExecutorService exec =
Executors.newCachedThreadPool();
static void test(Runnable r) throws InterruptedException{
Future<?> f = exec.submit(r);
TimeUnit.MILLISECONDS.sleep(100);
print("Interrupting " + r.getClass().getName());
f.cancel(true); // Interrupts if running
print("Interrupt sent to " + r.getClass().getName());
}
```

<!--p872-->
Concurrency
```java
public static void main(String[] args) throws Exception {
test(new SleepBlocked());
test(new IOBlocked(System.in));
test(new SynchronizedBlocked());
TimeUnit.SECONDS.sleep(3);
print("Aborting with System.exit(0)");
System.exit(0); // ... since last 2 interrupts failed
}
} /* Output: (95% match)
Interrupting SleepBlocked
InterruptedException
Exiting SleepBlocked.run()
Interrupt sent to SleepBlocked
Waiting for read():
Interrupting IOBlocked
Interrupt sent to IOBlocked
Trying to call f()
Interrupting SynchronizedBlocked
Interrupt sent to SynchronizedBlocked
Aborting with System.exit(0)
*///:~
```
Each task represents a different kind of blocking. SleepBlock is an example of interruptible blocking, whereas IOBlocked and SynchronizedBlocked are uninterruptible blocking.17 The program proves that I/O and waiting on a synchronized lock are not interruptible, but you can also anticipate this by looking at the code—no InterruptedException handler is required for either I/O or attempting to call a synchronized method. The first two classes are straightforward: The run( ) method calls sleep( ) in the first class and read( ) in the second. To demonstrate SynchronizedBlocked, however, we must first acquire the lock. This is accomplished in the constructor by creating an instance of an anonymous Thread class that acquires the object lock by calling f( ) (the thread must be different from the one driving run( ) for SynchronizedBlock because one thread can acquire an object lock multiple times). Since f( ) never returns, that lock is never released. SynchronizedBlock.run( ) attempts to call f( ) and is blocked waiting for the lock to be released. You’ll see from the output that you can interrupt a call to sleep( ) (or any call that requires you to catch InterruptedException). However, you cannot interrupt a task that is trying to acquire a synchronized lock or one that is trying to perform I/O. This is a little disconcerting, especially if you’re creating a task that performs I/O, because it means that I/O has the potential of locking your multithreaded program. Especially for Web-based programs, this is a concern. A heavy-handed but sometimes effective solution to this problem is to close the underlying resource on which the task is blocked:
```java
//: concurrency/CloseResource.java
// Interrupting a blocked task by
// closing the underlying resource.
// {RunByHand}
import java.net.*;
import java.util.concurrent.*;
import java.io.*;
import static net.mindview.util.Print.*;
```

<!--p873-->
17 Some releases of the JDK also provided support for InterruptedIOException. However, this was only partially implemented, and only on some platforms. If thisexception is thrown, it causes 10 objects to be unusable. Future releases are unlikely to continue support for this exception.
```java
public class CloseResource {
public static void main(String[] args) throws Exception {
ExecutorService exec = Executors.newCachedThreadPool();
ServerSocket server = new ServerSocket(8080);
InputStream socketInput =
new Socket("localhost", 8080).getInputStream();
exec.execute(new IOBlocked(socketInput));
exec.execute(new IOBlocked(System.in));
TimeUnit.MILLISECONDS.sleep(100);
print("Shutting down all threads");
exec.shutdownNow();
TimeUnit.SECONDS.sleep(1);
print("Closing " + socketInput.getClass().getName());
socketInput.close(); // Releases blocked thread
TimeUnit.SECONDS.sleep(1);
print("Closing " + System.in.getClass().getName());
System.in.close(); // Releases blocked thread
}
} /* Output: (85% match)
Waiting for read():
Waiting for read():
Shutting down all threads
Closing java.net.SocketInputStream
Interrupted from blocked I/O
Exiting IOBlocked.run()
Closing java.io.BufferedInputStream
Exiting IOBlocked.run()
*///:~
```
After shutdownNow( ) is called, the delays before calling close( ) on the two input streams emphasize that the tasks unblock once the underlying resource is closed. It’s interesting to note that the interrupt( ) appears when you are closing the Socket but not when closing System.in. Fortunately, the nio classes introduced in the I/O chapter provide for more civilized interruption of I/O. Blocked nio channels automatically respond to interrupts:
```java
//: concurrency/NIOInterruption.java
// Interrupting a blocked NIO channel.
import java.net.*;
import java.nio.*;
import java.nio.channels.*;
import java.util.concurrent.*;
import java.io.*;
import static net.mindview.util.Print.*;
class NIOBlocked implements Runnable {
private final SocketChannel sc;
public NIOBlocked(SocketChannel sc) { this.sc = sc; }
public void run() {
try {
print("Waiting for read() in " + this);
sc.read(ByteBuffer.allocate(1));
} catch(ClosedByInterruptException e) {
print("ClosedByInterruptException");
} catch(AsynchronousCloseException e) {
print("AsynchronousCloseException");
} catch(IOException e) {
throw new RuntimeException(e);
}
print("Exiting NIOBlocked.run() " + this);
}
```

<!--p874-->
Concurrency
```java
}
public class NIOInterruption {
public static void main(String[] args) throws Exception {
ExecutorService exec = Executors.newCachedThreadPool();
ServerSocket server = new ServerSocket(8080);
InetSocketAddress isa =
new InetSocketAddress("localhost", 8080);
SocketChannel sc1 = SocketChannel.open(isa);
SocketChannel sc2 = SocketChannel.open(isa);
Future<?> f = exec.submit(new NIOBlocked(sc1));
exec.execute(new NIOBlocked(sc2));
exec.shutdown();
TimeUnit.SECONDS.sleep(1);
// Produce an interrupt via cancel:
f.cancel(true);
TimeUnit.SECONDS.sleep(1);
// Release the block by closing the channel:
sc2.close();
}
} /* Output: (Sample)
Waiting for read() in NIOBlocked@7a84e4
Waiting for read() in NIOBlocked@15c7850
ClosedByInterruptException
Exiting NIOBlocked.run() NIOBlocked@15c7850
AsynchronousCloseException
Exiting NIOBlocked.run() NIOBlocked@7a84e4
*///:~
```
As shown, you can also close the underlying channel to release the block, although this should rarely be necessary. Note that using execute( ) to start both tasks and calling e.shutdownNow( ) will easily terminate everything; capturing the Future in the example above was only necessary to send the interrupt to one thread and not the other.18 Exercise 18:(2) Create a non-task class with a method that calls sleep( ) for a long interval. Create a task that calls the method in the non-task class. In main( ), start the task, then call interrupt( ) to terminate it. Make sure that the task shuts down safely. Exercise 19:(4) Modify OrnamentalGarden.java so that it uses interrupt( ). Exercise 20:(1) Modify CachedThreadPool.java so that all tasks receive an interrupt( ) before they are completed. Blocked by a mutex As you saw in Interrupting.java, if you try to call a synchronized method on an object whose lock has already been acquired, the calling task will be suspended (blocked) until the lock becomes available. The following example shows how the same mutex can be multiply acquired by the same task:
```java
//: concurrency/MultiLock.java
// One thread can reacquire the same lock.
import static net.mindview.util.Print.*;
public class MultiLock {
public synchronized void f1(int count) {
if(count-- > 0) {
```

<!--p875-->
18 Ervin Varga helped research this section.
```java
print("f1() calling f2() with count " + count);
f2(count);
}
}
public synchronized void f2(int count) {
if(count-- > 0) {
print("f2() calling f1() with count " + count);
f1(count);
}
}
public static void main(String[] args) throws Exception {
final MultiLock multiLock = new MultiLock();
new Thread() {
public void run() {
multiLock.f1(10);
}
}.start();
}
} /* Output:
f1() calling f2() with count 9
f2() calling f1() with count 8
f1() calling f2() with count 7
f2() calling f1() with count 6
f1() calling f2() with count 5
f2() calling f1() with count 4
f1() calling f2() with count 3
f2() calling f1() with count 2
f1() calling f2() with count 1
f2() calling f1() with count 0
*///:~
```
In main( ), a Thread is created to call f1( ), then f1( ) and f2( ) call each other until the count becomes zero. Since the task has already acquired the multiLock object lock inside the first call to f1( ), that same task is reacquiring it in the call to f2( ), and so on. This makes sense because one task should be able to call other synchronized methods within the same object; that task already holds the lock. As observed previously with uninterruptible I/O, anytime that a task can be blocked in such a way that it cannot be interrupted, you have the potential to lock up a program. One of the features added in the Java SE5 concurrency libraries is the ability for tasks blocked on ReentrantLocks to be interrupted, unlike tasks blocked on synchronized methods or critical sections:
```java
//: concurrency/Interrupting2.java
// Interrupting a task blocked with a ReentrantLock.
import java.util.concurrent.*;
import java.util.concurrent.locks.*;
import static net.mindview.util.Print.*;
class BlockedMutex {
private Lock lock = new ReentrantLock();
public BlockedMutex() {
// Acquire it right away, to demonstrate interruption
// of a task blocked on a ReentrantLock:
lock.lock();
}
public void f() {
try {
// This will never be available to a second task
lock.lockInterruptibly(); // Special call
print("lock acquired in f()");
} catch(InterruptedException e) {
```

<!--p876-->
Concurrency
```java
print("Interrupted from lock acquisition in f()");
}
}
}
class Blocked2 implements Runnable {
BlockedMutex blocked = new BlockedMutex();
public void run() {
print("Waiting for f() in BlockedMutex");
blocked.f();
print("Broken out of blocked call");
}
}
public class Interrupting2 {
public static void main(String[] args) throws Exception {
Thread t = new Thread(new Blocked2());
t.start();
TimeUnit.SECONDS.sleep(1);
System.out.println("Issuing t.interrupt()");
t.interrupt();
}
} /* Output:
Waiting for f() in BlockedMutex
Issuing t.interrupt()
Interrupted from lock acquisition in f()
Broken out of blocked call
*///:~
```

<!--p877-->
The class BlockedMutex has a constructor that acquires the object’s own Lock and never releases it. For that reason, if you try to call f( ) from a second task (different from the one that created the BlockedMutex), you will always be blocked because the Mutex cannot be acquired. In Blocked2, the run( ) method will be stopped at the call to blocked.f( ). When you run the program, you’ll see that, unlike an I/O call, interrupt( ) can break out of a call that’s blocked by a mutex.19 Checking for an interrupt Note that when you call interrupt( ) on a thread, the only time that the interrupt occurs is when the task enters, or is already inside, a blocking operation (except, as you’ve seen, in the case of uninterruptible I/O or blocked synchronized methods, in which case there’s nothing you can do). But what if you’ve written code that may or may not make such a blocking call, depending on the conditions in which it is run? If you can only exit by throwing an exception on a blocking call, you won’t always be able to leave the run( ) loop. Thus, if you call interrupt( ) to stop a task, your task needs a second way to exit in the event that your run( ) loop doesn’t happen to be making any blocking calls. This opportunity is presented by the interrupted status, which is set by the call to interrupt( ). You check for the interrupted status by calling interrupted( ). This not only tells you whether interrupt( ) has been called, it also clears the interrupted status. Clearing the interrupted status ensures that the framework will not notify you twice about a task being interrupted. You will be notified via either a single InterruptedException or a single successful Thread.interrupted( ) test. If you want to check again to see whether you were interrupted, you can store the result when you call Thread.interrupted( ). The following example shows the typical idiom that you should use in your run( ) method to handle both blocked and non-blocked possibilities when the interrupted status is set: 19 Note that, although it’s unlikely, the call to t.interrupt( ) could actually happen before the call to blocked.f( ).
```java
//: concurrency/InterruptingIdiom.java
// General idiom for interrupting a task.
// {Args: 1100}
import java.util.concurrent.*;
import static net.mindview.util.Print.*;
class NeedsCleanup {
private final int id;
public NeedsCleanup(int ident) {
id = ident;
print("NeedsCleanup " + id);
}
public void cleanup() {
print("Cleaning up " + id);
}
}
class Blocked3 implements Runnable {
private volatile double d = 0.0;
public void run() {
try {
while(!Thread.interrupted()) {
// point1
NeedsCleanup n1 = new NeedsCleanup(1);
// Start try-finally immediately after definition
// of n1, to guarantee proper cleanup of n1:
try {
print("Sleeping");
TimeUnit.SECONDS.sleep(1);
// point2
NeedsCleanup n2 = new NeedsCleanup(2);
// Guarantee proper cleanup of n2:
try {
print("Calculating");
// A time-consuming, non-blocking operation:
for(int i = 1; i < 2500000; i++)
d = d + (Math.PI + Math.E) / d;
print("Finished time-consuming operation");
} finally {
n2.cleanup();
}
} finally {
n1.cleanup();
}
}
print("Exiting via while() test");
} catch(InterruptedException e) {
print("Exiting via InterruptedException");
}
}
}
public class InterruptingIdiom {
public static void main(String[] args) throws Exception {
if(args.length != 1) {
print("usage: java InterruptingIdiom delay-in-mS");
System.exit(1);
}
Thread t = new Thread(new Blocked3());
t.start();
TimeUnit.MILLISECONDS.sleep(new Integer(args[0]));
t.interrupt();
}
```

<!--p878-->
Concurrency
```java
} /* Output: (Sample)
NeedsCleanup 1
Sleeping
NeedsCleanup 2
Calculating
Finished time-consuming operation
Cleaning up 2
Cleaning up 1
NeedsCleanup 1
Sleeping
Cleaning up 1
Exiting via InterruptedException
*///:~
```

<!--p879-->
The NeedsCleanup class emphasizes the necessity of proper resource cleanup if you leave the loop via an exception. Note that all NeedsCleanup resources created in Blocked3.run( ) must be immediately followed by try-finally clauses to guarantee that the cleanup( ) method is always called. You must give the program a command-line argument which is the delay time in milliseconds before it calls interrupt( ). By using different delays, you can exit Blocked3.run( ) at different points in the loop: in the blocking sleep( ) call, and in the non-blocking mathematical calculation. You’ll see that if interrupt( ) is called after the comment "point2" (during the non-blocking operation), first the loop is completed, then all the local objects are destroyed, and finally the loop is exited at the top via the while statement. However, if interrupt( ) is called between "pointi" and "point2" (after the while statement but before or during the blocking operation sleep( )), the task exits via the InterruptedException, the first time a blocking operation is attempted. In that case, only the NeedsCleanup objects that have been created up to the point where the exception is thrown are cleaned up, and you have the opportunity to perform any other cleanup in the catch clause. A class designed to respond to an interrupt( ) must establish a policy to ensure that it will remain in a consistent state. This generally means that the creation of all objects that require cleanup must be followed by try-finally clauses so that cleanup will occur regardless of how the run( ) loop exits. Code like this can work well, but alas, due to the lack of automatic destructor calls in Java, it relies on the client programmer to write the proper try-finally clauses. Cooperation between tasks As you’ve seen, when you use threads to run more than one task at a time, you can keep one task from interfering with another task’s resources by using a lock (mutex) to synchronize the behavior of the two tasks. That is, if two tasks are stepping on each other over a shared resource (usually memory), you use a mutex to allow only one task at a time to access that resource. With that problem solved, the next step is to learn how to make tasks cooperate with each other, so that multiple tasks can work together to solve a problem. Now the issue is not about interfering with one another, but rather about working in unison, since portions of such problems must be solved before other portions can be solved. It’s much like project planning: The footings for the house must be dug first, but the steel can be laid and the concrete forms can be built in parallel, and both of those tasks must be finished before the concrete foundation can be poured. The plumbing must be in place before the concrete slab can be poured, the concrete slab must be in place before you start framing, and so on. Some of these tasks can be done in parallel, but certain steps require all tasks to be completed before you can move ahead. The key issue when tasks are cooperating is handshaking between those tasks. To accomplish this handshaking, we use the same foundation: the mutex, which in this case guarantees that only one task can respond to a signal. This eliminates any possible race conditions. On top of the mutex, we add a way for a task to suspend itself until some external state changes (e.g., "The plumbing is now in place"), indicating that it’s time for that task to move forward. In this section, we’ll look at the issues of handshaking between tasks, which is safely implemented using the Object methods wait( ) and notifyAll( ). The Java SE5 concurrency library also provides Condition objects with await( ) and signal( ) methods. We’ll see the problems that can arise, and their solutions.
## wait() and notifyAll()

<!--p880-->
wait( ) allows you to wait for a change in some condition that is outside the control of the forces in the current method. Often, this condition will be changed by another task. You don’t want to idly loop while testing the condition inside your task; this is called busy waiting, and it’s usually a bad use of CPU cycles. So wait( ) suspends the task while waiting for the world to change, and only when a notify( ) or notifyAll( ) occurs—suggesting that something of interest may have happened—does the task wake up and check for changes. Thus, wait( ) provides a way to synchronize activities between tasks. It’s important to understand that sleep( ) does not release the object lock when it is called, and neither does yield( ). On the other hand, when a task enters a call to wait( ) inside a method, that thread’s execution is suspended, and the lock on that object is released. Because wait( ) releases the lock, it means that the lock can be acquired by another task, so other synchronized methods in the (now unlocked) object can be called during a wait( ). This is essential, because those other methods are typically what cause the change that makes it interesting for the suspended task to reawaken. Thus, when you call wait( ), you’re saying, "I’ve done all I can right now, so I’m going to wait right here, but I want to allow other synchronized operations to take place if they can." There are two forms of wait( ). One version takes an argument in milliseconds that has the same meaning as in sleep( ): "Pause for this period of time." But unlike with sleep( ), with wait(pause): 1.The object lock is released during the wait( ). 2.You can also come out of the wait( ) due to a notify( ) or notifyAll( ), in addition to letting the clock run out. The second, more commonly used form of wait( ) takes no arguments. This wait( ) continues indefinitely until the thread receives a notify( ) or notifyAll( ). One fairly unique aspect of wait( ), notify( ), and notifyAll( ) is that these methods are part of the base class Object and not part of Thread. Although this seems a bit strange at first—to have something that’s exclusively for threading as part of the universal base class— it’s essential because these methods manipulate the lock that’s also part of every object. As a result, you can put a wait( ) inside any synchronized method, regardless of whether that class extends Thread or implements Runnable. In fact, the only place you can call wait( ), notify( ), or notifyAll( ) is within a synchronized method or block (sleep( ) can be called within non-synchronized methods since it doesn’t manipulate the lock). If you call any of these within a method that’s not synchronized, the program will compile, but when you run it, you’ll get an IllegalMonitorStateException with the somewhat nonintuitive message "current thread not owner." This message means that the task calling wait( ), notify( ), or notifyAll( ) must "own" (acquire) the lock for the object before it can call any of those methods. Concurrency You can ask another object to perform an operation that manipulates its own lock. To do this, you must first capture that object’s lock. For example, if you want to send notifyAll( ) to an object x, you must do so inside a synchronized block that acquires the lock for x:
```java
synchronized(x) {
x.notifyAll();
}
```
Let’s look at a simple example. WaxOMatic.java has two processes: one to apply wax to a Car and one to polish it. The polishing task cannot do its job until the application task is finished, and the application task must wait until the polishing task is finished before it can put on another coat of wax. Both WaxOn and WaxOff use the Car object, which uses wait( ) and notifyAll( ) to suspend and restart tasks while they’re waiting for a condition to change:

<!--p881-->
```java
//: concurrency/waxomatic/WaxOMatic.java
// Basic task cooperation.
package concurrency.waxomatic;
import java.util.concurrent.*;
import static net.mindview.util.Print.*;
class Car {
private boolean waxOn = false;
public synchronized void waxed() {
waxOn = true; // Ready to buff
notifyAll();
}
public synchronized void buffed() {
waxOn = false; // Ready for another coat of wax
notifyAll();
}
public synchronized void waitForWaxing()
throws InterruptedException {
while(waxOn == false)
wait();
}
public synchronized void waitForBuffing()
throws InterruptedException {
while(waxOn == true)
wait();
}
}
class WaxOn implements Runnable {
private Car car;
public WaxOn(Car c) { car = c; }
public void run() {
try {
while(!Thread.interrupted()) {
printnb("Wax On! ");
TimeUnit.MILLISECONDS.sleep(200);
car.waxed();
car.waitForBuffing();
}
} catch(InterruptedException e) {
print("Exiting via interrupt");
}
print("Ending Wax On task");
}
}
class WaxOff implements Runnable {
```
Concurrency
```java
private Car car;
public WaxOff(Car c) { car = c; }
public void run() {
try {
while(!Thread.interrupted()) {
car.waitForWaxing();
printnb("Wax Off! ");
TimeUnit.MILLISECONDS.sleep(200);
car.buffed();
}
} catch(InterruptedException e) {
print("Exiting via interrupt");
}
print("Ending Wax Off task");
}
}
public class WaxOMatic {
public static void main(String[] args) throws Exception {
Car car = new Car();
ExecutorService exec = Executors.newCachedThreadPool();
exec.execute(new WaxOff(car));
exec.execute(new WaxOn(car));
TimeUnit.SECONDS.sleep(5); // Run for a while...
exec.shutdownNow(); // Interrupt all tasks
}
} /* Output: (95% match)
Wax On! Wax Off! Wax On! Wax Off! Wax On! Wax Off! Wax On! Wax Off! Wax
On! Wax Off! Wax On! Wax Off! Wax On! Wax Off! Wax On! Wax Off! Wax On!
Wax Off! Wax On! Wax Off! Wax On! Wax Off! Wax On! Wax Off! Wax On!
Exiting via interrupt
Ending Wax On task
Exiting via interrupt
Ending Wax Off task
*///:~
```

<!--p882-->
Here, Car has a single boolean waxOn, which indicates the state of the waxing-polishing process. In waitForWaxing( ), the waxOn flag is checked, and if it is false, the calling task is suspended by calling wait( ). It’s important that this occur in a synchronized method, where the task has acquired the lock. When you call wait( ), the thread is suspended and the lock is released. It is essential that the lock be released because, to safely change the state of the object (for example, to change waxOn to true, which must happen if the suspended task is to ever continue), that lock must be available to be acquired by some other task. In this example, when another task calls waxed( ) to indicate that it’s time to do something, the lock must be acquired in order to change waxOn to true. Afterward, waxed( ) calls notifyAll( ), which wakes up the task that was suspended in the call to wait( ). In order for the task to wake up from a wait( ), it must first reacquire the lock that it released when it entered the wait( ). The task will not wake up until that lock becomes available.20 WaxOn.run( ) represents the first step in the process of waxing the car, so it performs its operation: a call to sleep( ) to simulate the time necessary for waxing. It then tells the car that waxing is complete, and calls waitForBuffing( ), which suspends this task with a 20On some platforms there’s a third way to come out of a wait( ): the so-called spurious wake-up. A spurious wake-up essentially means that a thread may prematurely stop blocking (while waiting on a condition variable or semaphore) without being prompted by a notify( ) or notifyAll( ) (or their equivalents for the new Condition objects). The thread just wakes up, seemingly by itself. Spurious wake-ups exist because implementing POSIX threads, or the equivalent, isn’t always as straightforward as it should be on some platforms. Allowing spurious wake-ups makes the job of building a library like pthreads easier for those platforms. wait( ) until the WaxOff task calls buffed( ) for the car, changing the state and calling notifyAll( ). WaxOff.run( ), on the other hand, immediately moves into waitForWaxing( ) and is thus suspended until the wax has been applied by WaxOn and waxed( ) is called. When you run this program, you can watch this two-step process repeat itself as control is handed back and forth between the two tasks. After five seconds, interrupt( ) halts both threads; when you call shutdownNow( ) for an ExecutorService, it calls interrupt( ) for all the tasks it is controlling. The previous example emphasizes that you must surround a wait( ) with a while loop that checks the condition(s) of interest. This is important because: • You may have multiple tasks waiting on the same lock for the same reason, and the first task that wakes up might change the situation (even if you don’t do this someone might inherit from your class and do it). If that is the case, this task should be suspended again until its condition of interest changes. • By the time this task awakens from its wait( ), it’s possible that some other task will have changed things such that this task is unable to perform or is uninterested in performing its operation at this time. Again, it should be resuspended by calling wait( ) again. • It’s also possible that tasks could be waiting on your object’s lock for different reasons (in which case you must use notifyAll( )). In this case, you need to check whether you’ve been woken up for the right reason, and if not, call wait( ) again. Thus, it’s essential that you check for your particular condition of interest, and go back into wait( ) if that condition is not met. This is idiomatically written using a while. Exercise 21:(2) Create two Runnables, one with a run( ) that starts and calls wait( ). The second class should capture the reference of the first Runnable object. Its run( ) should call notifyAll( ) for the first task after some number of seconds have passed so that the first task can display a message. Test your classes using an Executor. Exercise 22:(4) Create an example of a busy wait. One task sleeps for a while and then sets a flag to true. The second task watches that flag inside a while loop (this is the busy wait) and when the flag becomes true, sets it back to false and reports the change to the console. Note how much wasted time the program spends inside the busy wait, and create a second version of the program that uses wait( ) instead of the busy wait. Missed Signals When two threads are coordinated using notify( )/wait( ) or notifyAll( )/wait( ), it’s possible to miss a signal. Suppose T1 is a thread that notifies T2, and that the two threads are implemented using the following (flawed) approach:

<!--p883-->
```java
T1:
synchronized(sharedMonitor) {
<setup condition for T2>
sharedMonitor.notify();
}
T2:
while(someCondition) {
// Point 1
synchronized(sharedMonitor) {
sharedMonitor.wait();
}
}
```
The <setup condition for T2> is an action to prevent T2 from calling wait( ), if it hasn’t already. Assume that T2 evaluates someCondition and finds it true. At Point 1, the thread scheduler might switch to T1. T1 executes its setup, and then calls notify( ). When T2 continues executing, it is too late for T2 to realize that the condition has been changed in the meantime, and it will blindly enter wait( ). The notify( ) will be missed and T2 will wait indefinitely for the signal that was already sent, producing deadlock. The solution is to prevent the race condition over the someCondition variable. Here is the correct approach for T2:
```java
synchronized(sharedMonitor) {
while(someCondition)
sharedMonitor.wait();
}
```
Now, if T1 executes first, when control returns back to T2 it will figure out that the condition has changed, and will not enter wait( ). Conversely, if T2 executes first, it will enter wait( ) and later be awakened by T1. Thus, the signal cannot be missed.
## notify() vs. notifyAll()
Because more than one task could technically be in a wait( ) on a single Car object, it is safer to call notifyAll( ) rather than just notify( ). However, the structure of the above program is such that only one task will actually be in a wait( ), so you could use notify( ) instead of notifyAll( ). Using notify( ) instead of notifyAll( ) is an optimization. Only one task of the possible many that are waiting on a lock will be awoken with notify( ), so you must be certain that the right task will wake up if you try to use notify( ). In addition, all tasks must be waiting on the same condition in order for you to use notify( ), because if you have tasks that are waiting on different conditions, you don’t know if the right one will wake up. If you use notify( ), only one task must benefit when the condition changes. Finally, these constraints must always be true for all possible subclasses. If any of these rules cannot be met, you must use notifyAll( ) rather than notify( ). One of the confusing statements often made in discussions of Java threading is that notifyAll( ) wakes up "all waiting tasks." Does this mean that any task that is in a wait( ), anywhere in the program, is awoken by any call to notifyAll( )? In the following example, the code associated with Task2 shows that this is not true—in fact, only the tasks that are waiting on a particular lock are awoken when notifyAll( ) is called/or that lock:
```java
//: concurrency/NotifyVsNotifyAll.java
import java.util.concurrent.*;
import java.util.*;
class Blocker {
synchronized void waitingCall() {
try {
while(!Thread.interrupted()) {
wait();
System.out.print(Thread.currentThread() + " ");
}
} catch(InterruptedException e) {
// OK to exit this way
}
}
```

<!--p884-->
Concurrency

<!--p885-->
```java
synchronized void prod() { notify(); }
synchronized void prodAll() { notifyAll(); }
}
class Task implements Runnable {
static Blocker blocker = new Blocker();
public void run() { blocker.waitingCall(); }
}
class Task2 implements Runnable {
// A separate Blocker object:
static Blocker blocker = new Blocker();
public void run() { blocker.waitingCall(); }
}
public class NotifyVsNotifyAll {
public static void main(String[] args) throws Exception {
ExecutorService exec = Executors.newCachedThreadPool();
for(int i = 0; i < 5; i++)
exec.execute(new Task());
exec.execute(new Task2());
Timer timer = new Timer();
timer.scheduleAtFixedRate(new TimerTask() {
boolean prod = true;
public void run() {
if(prod) {
System.out.print("\nnotify() ");
Task.blocker.prod();
prod = false;
} else {
System.out.print("\nnotifyAll() ");
Task.blocker.prodAll();
prod = true;
}
}
}, 400, 400); // Run every .4 second
TimeUnit.SECONDS.sleep(5); // Run for a while...
timer.cancel();
System.out.println("\nTimer canceled");
TimeUnit.MILLISECONDS.sleep(500);
System.out.print("Task2.blocker.prodAll() ");
Task2.blocker.prodAll();
TimeUnit.MILLISECONDS.sleep(500);
System.out.println("\nShutting down");
exec.shutdownNow(); // Interrupt all tasks
}
} /* Output: (Sample)
notify() Thread[pool-1-thread-1,5,main]
notifyAll() Thread[pool-1-thread-1,5,main] Thread[pool-1-thread-
5,5,main] Thread[pool-1-thread-4,5,main] Thread[pool-1-thread-3,5,main]
Thread[pool-1-thread-2,5,main]
notify() Thread[pool-1-thread-1,5,main]
notifyAll() Thread[pool-1-thread-1,5,main] Thread[pool-1-thread-
2,5,main] Thread[pool-1-thread-3,5,main] Thread[pool-1-thread-4,5,main]
Thread[pool-1-thread-5,5,main]
notify() Thread[pool-1-thread-1,5,main]
notifyAll() Thread[pool-1-thread-1,5,main] Thread[pool-1-thread-
5,5,main] Thread[pool-1-thread-4,5,main] Thread[pool-1-thread-3,5,main]
Thread[pool-1-thread-2,5,main]
notify() Thread[pool-1-thread-1,5,main]
notifyAll() Thread[pool-1-thread-1,5,main] Thread[pool-1-thread-
2,5,main] Thread[pool-1-thread-3,5,main] Thread[pool-1-thread-4,5,main]
Thread[pool-1-thread-5,5,main]
notify() Thread[pool-1-thread-1,5,main]
notifyAll() Thread[pool-1-thread-1,5,main] Thread[pool-1-thread-
5,5,main] Thread[pool-1-thread-4,5,main] Thread[pool-1-thread-3,5,main]
Thread[pool-1-thread-2,5,main]
notify() Thread[pool-1-thread-1,5,main]
notifyAll() Thread[pool-1-thread-1,5,main] Thread[pool-1-thread-
2,5,main] Thread[pool-1-thread-3,5,main] Thread[pool-1-thread-4,5,main]
Thread[pool-1-thread-5,5,main]
Timer canceled
Task2.blocker.prodAll() Thread[pool-1-thread-6,5,main]
Shutting down
*///:~
```
Task and Task2 each have their own Blocker object, so each Task object blocks on Task.blocker, and each Task2 object blocks on Task2.blocker. In main( ), a java.util.Timer object is set up to execute its run( ) method every 4/10 of a second, and that run( ) alternates between calling notify( ) and notifyAll( ) on Task.blocker via the "prod" methods. From the output, you can see that even though a Task2 object exists and is blocked on Task2.blocker, none of the notify( ) or notifyAll( ) calls on Task.blocker causes the Task2 object to wake up. Similarly, at the end of main( ), cancel( ) is called for the timer, and even though the timer is canceled, the first five tasks are still running and still blocked in their calls to Task.blocker.waitingCall( ). The output from the call to Task2.blocker.prodAll( ) does nor include any of the tasks waiting on the lock in Task.blocker. This also makes sense if you look at prod( ) and prodAll( ) in Blocker. These methods are synchronized, which means that they acquire their own lock, so when they call notify( ) or notifyAll( ), it’s logical that they are only calling it for that lock—and thus only wake up tasks that are waiting on that particular lock. Blocker.waitingCall( ) is simple enough that you could just say for(;;) instead of while(!Thread.interrupted( )), and achieve the same effect in this case, because in this example there’s no difference between leaving the loop with an exception and leaving it by checking the interrupted( ) flag— the same code is executed in both cases. As a matter of form, however, this example checks interrupted( ), because there are two different ways of leaving the loop. If, sometime later, you decide to add more code to the loop, you risk introducing an error if you don’t cover both paths of exit from the loop. Exercise 23:(7) Demonstrate that WaxOMatic.java works successfully when you use notify( ) instead of notifyAll( ). Producers and consumers Consider a restaurant that has one chef and one waitperson. The waitperson must wait for the chef to prepare a meal. When the chef has a meal ready, the chef notifies the waitperson, who then gets and delivers the meal and goes back to waiting. This is an example of task cooperation: The chef represents the producer, and the waitperson represents the consumer. Both tasks must handshake with each other as meals are produced and consumed, and the system must shut down in an orderly fashion. Here is the story modeled in code:
```java
//: concurrency/Restaurant.java
// The producer-consumer approach to task cooperation.
import java.util.concurrent.*;
import static net.mindview.util.Print.*;
class Meal {
```

<!--p886-->
Concurrency

<!--p887-->
```java
private final int orderNum;
public Meal(int orderNum) { this.orderNum = orderNum; }
public String toString() { return "Meal " + orderNum; }
}
class WaitPerson implements Runnable {
private Restaurant restaurant;
public WaitPerson(Restaurant r) { restaurant = r; }
public void run() {
try {
while(!Thread.interrupted()) {
synchronized(this) {
while(restaurant.meal == null)
wait(); // ... for the chef to produce a meal
}
print("Waitperson got " + restaurant.meal);
synchronized(restaurant.chef) {
restaurant.meal = null;
restaurant.chef.notifyAll(); // Ready for another
}
}
} catch(InterruptedException e) {
print("WaitPerson interrupted");
}
}
}
class Chef implements Runnable {
private Restaurant restaurant;
private int count = 0;
public Chef(Restaurant r) { restaurant = r; }
public void run() {
try {
while(!Thread.interrupted()) {
synchronized(this) {
while(restaurant.meal != null)
wait(); // ... for the meal to be taken
}
if(++count == 10) {
print("Out of food, closing");
restaurant.exec.shutdownNow();
}
printnb("Order up! ");
synchronized(restaurant.waitPerson) {
restaurant.meal = new Meal(count);
restaurant.waitPerson.notifyAll();
}
TimeUnit.MILLISECONDS.sleep(100);
}
} catch(InterruptedException e) {
print("Chef interrupted");
}
}
}
public class Restaurant {
Meal meal;
ExecutorService exec = Executors.newCachedThreadPool();
WaitPerson waitPerson = new WaitPerson(this);
Chef chef = new Chef(this);
public Restaurant() {
exec.execute(chef);
exec.execute(waitPerson);
}
public static void main(String[] args) {
new Restaurant();
}
} /* Output:
Order up! Waitperson got Meal 1
Order up! Waitperson got Meal 2
Order up! Waitperson got Meal 3
Order up! Waitperson got Meal 4
Order up! Waitperson got Meal 5
Order up! Waitperson got Meal 6
Order up! Waitperson got Meal 7
Order up! Waitperson got Meal 8
Order up! Waitperson got Meal 9
Out of food, closing
WaitPerson interrupted
Order up! Chef interrupted
*///:~
```
The Restaurant is the focal point for both the WaitPerson and the Chef. Both must know what Restaurant they are working for because they must place or fetch the meal from the restaurant’s "meal window," restaurant.meal. In run( ), the WaitPerson goes into wait( ) mode, stopping that task until it is woken up with a notifyAll( ) from the Chef. Since this is a very simple program, we know that only one task will be waiting on the WaitPerson’slock: the WaitPerson task itself. For this reason, it’s theoretically possible to call notify( ) instead of notifyAll( ). However, in more complex situations, multiple tasks may be waiting on a particular object lock, so you don’t know which task should be awakened. Thus, it’s safer to call notifyAll( ), which wakes up all the tasks waiting on that lock. Each task must then decide whether the notification is relevant. Once the Chef delivers a Meal and notifies the WaitPerson, the Chef waits until the WaitPerson collects the meal and notifies the Chef, who can then produce the next Meal. Notice that the wait( ) is wrapped in a while( ) statement that is testing for the same thing that is being waited for. This seems a bit strange at first—if you’re waiting for an order, once you wake up, the order must be available, right? As noted earlier, the problem is that in a concurrent application, some other task might swoop in and grab the order while the WaitPerson is waking up. The only safe approach is to always use the following idiom for a wait( ) (within proper synchronization, of course, and programming against the possibility of missed signals):
```java
while(conditionlsNotMet)
wait();
```

<!--p888-->
This guarantees that the condition will be met before you get out of the wait loop, and if you have been notified of something that doesn’t concern the condition (as can happen with notifyAll( )), or the condition changes before you get fully out of the wait loop, you are guaranteed to go back into waiting. Observe that the call to notifyAll( ) must first capture the lock on waitPerson. The call to wait( ) in WaitPerson.run( ) automatically releases the lock, so this is possible. Because the lock must be owned in order for notifyAll( ) to be called, it’s guaranteed that two tasks trying to call notifyAll( ) on one object won’t step on each other’s toes. Both run( ) methods are designed for orderly shutdown by enclosing the entire run( ) with a try block. The catch clause closes right before the closing brace of the run( ) method, so if the task receives an InterruptedException, it ends immediately after catching the exception. Concurrency In Chef, note that after calling shutdownNow( ) you could simply return from run( ), and normally that’s what you should do. However, it’s a little more interesting to do it this way. Remember that shutdownNow( ) sends an interrupt( ) to all the tasks that the ExecutorService started. But in the case of the Chef, the task doesn’t shut down immediately upon getting the interrupt( ), because the interrupt only throws InterruptedException as the task attempts to enter an (interruptible) blocking operation. Thus, you’ll see "Order up!" displayed first, and then the InterruptedException is thrown when the Chef attempts to call sleep( ). If you remove the call to sleep( ), the task will get to the top of the run( ) loop and exit because of the Thread.interrupted( ) test, without throwing an exception. The preceding example has only a single spot for one task to store an object so that another task can later use that object. However, in a typical producerconsumer implementation, you use a first-in, first-out queue in order to store the objects being produced and consumed. You’ll learn more about such queues later in this chapter. Exercise 24:(1) Solve a single-producer, single-consumer problem using wait( ) and notifyAll( ). The producer must not overflow the receiver’s buffer, which can happen if the producer is faster than the consumer. If the consumer is faster than the producer, then it must not read the same data more than once. Do not assume anything about the relative speeds of the producer or consumer. Exercise 25:(1) Inthe Chef class in Restaurant.java, return from run( ) after calling shutdownNow( ) and observe the difference in behavior. Exercise 26:(8) Add a BusBoy class to Restaurant.java. After the meal is delivered, the WaitPerson should notify the BusBoy to clean up.
## Using explicit Lock and Condition objects
There are additional, explicit tools in the Java SE5 java.util.concurrent library that can be used to rewrite WaxOMatic.java. The basic class that uses a mutex and allows task suspension is the Condition, and you can suspend a task by calling await( ) on a Condition. When external state changes take place that might mean that a task should continue processing, you notify the task by calling signal( ), to wake up one task, or signalAll( ), to wake up all tasks that have suspended themselves on that Condition object (as with notifyAll( ), signalAll( ) is the safer approach). Here’s WaxOMatic.java rewritten to contain a Condition that it uses to suspend a task inside waitForWaxing( ) or waitForBuffing( ):

<!--p889-->
```java
//: concurrency/waxomatic2/WaxOMatic2.java
// Using Lock and Condition objects.
package concurrency.waxomatic2;
import java.util.concurrent.*;
import java.util.concurrent.locks.*;
import static net.mindview.util.Print.*;
class Car {
private Lock lock = new ReentrantLock();
private Condition condition = lock.newCondition();
private boolean waxOn = false;
public void waxed() {
lock.lock();
try {
waxOn = true; // Ready to buff
condition.signalAll();
} finally {
lock.unlock();
}
}
public void buffed() {
lock.lock();
try {
waxOn = false; // Ready for another coat of wax
condition.signalAll();
} finally {
lock.unlock();
}
}
public void waitForWaxing() throws InterruptedException {
lock.lock();
try {
while(waxOn == false)
condition.await();
} finally {
lock.unlock();
}
}
public void waitForBuffing() throws InterruptedException{
lock.lock();
try {
while(waxOn == true)
condition.await();
} finally {
lock.unlock();
}
}
}
class WaxOn implements Runnable {
private Car car;
public WaxOn(Car c) { car = c; }
public void run() {
try {
while(!Thread.interrupted()) {
printnb("Wax On! ");
TimeUnit.MILLISECONDS.sleep(200);
car.waxed();
car.waitForBuffing();
}
} catch(InterruptedException e) {
print("Exiting via interrupt");
}
print("Ending Wax On task");
}
}
class WaxOff implements Runnable {
private Car car;
public WaxOff(Car c) { car = c; }
public void run() {
try {
while(!Thread.interrupted()) {
car.waitForWaxing();
printnb("Wax Off! ");
TimeUnit.MILLISECONDS.sleep(200);
car.buffed();
}
} catch(InterruptedException e) {
print("Exiting via interrupt");
```

<!--p890-->
Concurrency
```java
}
print("Ending Wax Off task");
}
}
public class WaxOMatic2 {
public static void main(String[] args) throws Exception {
Car car = new Car();
ExecutorService exec = Executors.newCachedThreadPool();
exec.execute(new WaxOff(car));
exec.execute(new WaxOn(car));
TimeUnit.SECONDS.sleep(5);
exec.shutdownNow();
}
} /* Output: (90% match)
Wax On! Wax Off! Wax On! Wax Off! Wax On! Wax Off! Wax On! Wax Off! Wax
On! Wax Off! Wax On! Wax Off! Wax On! Wax Off! Wax On! Wax Off! Wax On!
Wax Off! Wax On! Wax Off! Wax On! Wax Off! Wax On! Wax Off! Wax On!
Exiting via interrupt
Ending Wax Off task
Exiting via interrupt
Ending Wax On task
*///:~
```

<!--p891-->
In Car’s constructor, a single Lock produces a Condition object which is used to manage inter-task communication. However, the Condition object contains no information about the state of the process, so you need to manage additional information to indicate process state, which is the boolean waxOn. Each call to lock( ) must immediately be followed by a try-finally clause to guarantee that unlocking happens in all cases. As with the built-in versions, a task must own the lock before it can call await( ), signal( ) or signalAll( ). Notice that this solution is more complex than the previous one, and the complexity doesn’t gain you anything in this case. The Lock and Condition objects are only necessary for more difficult threading problems. Exercise 27:(2) Modify Restaurant.java to use explicit Lock and Condition objects. Producer-consumers and queues The wait( ) and notifyAll( ) methods solve the problem of task cooperation in a rather low- level fashion, handshaking every interaction. In many cases, you can move up a level of abstraction and solve task cooperation problems using a synchronized queue, which only allows one task at a time to insert or remove an element. This is provided for you in the java.util.concurrent.BlockingQueue interface, which has a number of standard implementations. You’ll usually use the LinkedBlockingQueue, which is an unbounded queue; the ArrayBlockingQueue has a fixed size, so you can only put so many elements in it before it blocks. These queues also suspend a consumer task if that task tries to get an object from the queue and the queue is empty, and resume when more elements become available. Blocking queues can solve a remarkable number of problems in a much simpler and more reliable fashion than wait( ) and notifyAll( ). Here’s a simple test that serializes the execution of LiftOff objects. The consumer is LiftOffRunner, which pulls each LiftOff object off the BlockingQueue and runs it directly. (That is, it uses its own thread by calling run( ) explicitly rather than starting up a new thread for each task.)
```java
//: concurrency/TestBlockingQueues.java
// {RunByHand}
import java.util.concurrent.*;
import java.io.*;
import static net.mindview.util.Print.*;
class LiftOffRunner implements Runnable {
private BlockingQueue<LiftOff> rockets;
public LiftOffRunner(BlockingQueue<LiftOff> queue) {
rockets = queue;
}
public void add(LiftOff lo) {
try {
rockets.put(lo);
} catch(InterruptedException e) {
print("Interrupted during put()");
}
}
public void run() {
try {
while(!Thread.interrupted()) {
LiftOff rocket = rockets.take();
rocket.run(); // Use this thread
}
} catch(InterruptedException e) {
print("Waking from take()");
}
print("Exiting LiftOffRunner");
}
}
public class TestBlockingQueues {
static void getkey() {
try {
// Compensate for Windows/Linux difference in the
// length of the result produced by the Enter key:
new BufferedReader(
new InputStreamReader(System.in)).readLine();
} catch(java.io.IOException e) {
throw new RuntimeException(e);
}
}
static void getkey(String message) {
print(message);
getkey();
}
static void
test(String msg, BlockingQueue<LiftOff> queue) {
print(msg);
LiftOffRunner runner = new LiftOffRunner(queue);
Thread t = new Thread(runner);
t.start();
for(int i = 0; i < 5; i++)
runner.add(new LiftOff(5));
getkey("Press ‘Enter’ (" + msg + ")");
t.interrupt();
print("Finished " + msg + " test");
}
public static void main(String[] args) {
test("LinkedBlockingQueue", // Unlimited size
```

<!--p892-->
Concurrency
```java
new LinkedBlockingQueue<LiftOff>());
test("ArrayBlockingQueue", // Fixed size
new ArrayBlockingQueue<LiftOff>(3));
test("SynchronousQueue", // Size of 1
new SynchronousQueue<LiftOff>());
}
} ///:~
```
The tasks are placed on the BlockingQueue by main( ) and are taken off the BlockingQueue bythe LiftOffRunner. Notice that LiftOffRunner can ignore synchronization issues because they are solved by the BlockingQueue. Exercise 28:(3) Modify TestBlockingQueues.java by adding a new task that places LiftOff on the BlockingQueue, instead of doing it in main( ).
## BlockingQueues of toast
As an example of the use of BlockingQueues, consider a machine that has three tasks: one to make toast, one to butter the toast, and one to put jam on the buttered toast. We can run the toast through BlockingQueues between processes:

<!--p893-->
```java
//: concurrency/ToastOMatic.java
// A toaster that uses queues.
import java.util.concurrent.*;
import java.util.*;
import static net.mindview.util.Print.*;
class Toast {
public enum Status { DRY, BUTTERED, JAMMED }
private Status status = Status.DRY;
private final int id;
public Toast(int idn) { id = idn; }
public void butter() { status = Status.BUTTERED; }
public void jam() { status = Status.JAMMED; }
public Status getStatus() { return status; }
public int getId() { return id; }
public String toString() {
return "Toast " + id + ": " + status;
}
}
class ToastQueue extends LinkedBlockingQueue<Toast> {}
class Toaster implements Runnable {
private ToastQueue toastQueue;
private int count = 0;
private Random rand = new Random(47);
public Toaster(ToastQueue tq) { toastQueue = tq; }
public void run() {
try {
while(!Thread.interrupted()) {
TimeUnit.MILLISECONDS.sleep(
100 + rand.nextInt(500));
// Make toast
Toast t = new Toast(count++);
print(t);
// Insert into queue
toastQueue.put(t);
}
} catch(InterruptedException e) {
print("Toaster interrupted");
}
print("Toaster off");
}
}
// Apply butter to toast:
class Butterer implements Runnable {
private ToastQueue dryQueue, butteredQueue;
public Butterer(ToastQueue dry, ToastQueue buttered) {
dryQueue = dry;
butteredQueue = buttered;
}
public void run() {
try {
while(!Thread.interrupted()) {
// Blocks until next piece of toast is available:
Toast t = dryQueue.take();
t.butter();
print(t);
butteredQueue.put(t);
}
} catch(InterruptedException e) {
print("Butterer interrupted");
}
print("Butterer off");
}
}
// Apply jam to buttered toast:
class Jammer implements Runnable {
private ToastQueue butteredQueue, finishedQueue;
public Jammer(ToastQueue buttered, ToastQueue finished) {
butteredQueue = buttered;
finishedQueue = finished;
}
public void run() {
try {
while(!Thread.interrupted()) {
// Blocks until next piece of toast is available:
Toast t = butteredQueue.take();
t.jam();
print(t);
finishedQueue.put(t);
}
} catch(InterruptedException e) {
print("Jammer interrupted");
}
print("Jammer off");
}
}
// Consume the toast:
class Eater implements Runnable {
private ToastQueue finishedQueue;
private int counter = 0;
public Eater(ToastQueue finished) {
finishedQueue = finished;
}
public void run() {
try {
while(!Thread.interrupted()) {
// Blocks until next piece of toast is available:
Toast t = finishedQueue.take();
```

<!--p894-->
Concurrency
```java
// Verify that the toast is coming in order,
// and that all pieces are getting jammed:
if(t.getId() != counter++ ||
t.getStatus() != Toast.Status.JAMMED) {
print(">>>> Error: " + t);
System.exit(1);
} else
print("Chomp! " + t);
}
} catch(InterruptedException e) {
print("Eater interrupted");
}
print("Eater off");
}
}
public class ToastOMatic {
public static void main(String[] args) throws Exception {
ToastQueue dryQueue = new ToastQueue(),
butteredQueue = new ToastQueue(),
finishedQueue = new ToastQueue();
ExecutorService exec = Executors.newCachedThreadPool();
exec.execute(new Toaster(dryQueue));
exec.execute(new Butterer(dryQueue, butteredQueue));
exec.execute(new Jammer(butteredQueue, finishedQueue));
exec.execute(new Eater(finishedQueue));
TimeUnit.SECONDS.sleep(5);
exec.shutdownNow();
}
} /* (Execute to see output) *///:~
```
Toast is an excellent example of the value of enums. Note that there is no explicit synchronization (using Lock objects or the synchronized keyword) because the synchronization is implicitly managed by the queues (which synchronize internally) and by the design of the system—each piece of Toast is only operated on by one task at a time. Because the queues block, processes suspend and resume automatically. You can see that the simplification produced by BlockingQueuescan be quite dramatic. The coupling between the classes that would exist with explicit wait( ) and notifyAll( ) statements is eliminated because each class communicates only with its BlockingQueues. Exercise 29:(8) Modify ToastOMatic.java to create peanut butter and jelly on toast sandwiches using two separate assembly lines (one for peanut butter, the second for jelly, then merging the two lines). Using pipes for I/O between tasks It’s often useful for tasks to communicate with each other using I/O. Threading libraries may provide support for inter-task I/O in the form of pipes. These exist in the Java I/O library as the classes PipedWriter (which allows a task to write into a pipe) and PipedReader (which allows a different task to read from the same pipe). This can be thought of as a variation of the producer-consumer problem, where the pipe is the canned solution. The pipe is basically a blocking queue, which existed in versions of Java before BlockingQueue was introduced. Here’s a simple example in which two tasks use a pipe to communicate:

<!--p895-->
```java
//: concurrency/PipedIO.java
// Using pipes for inter-task I/O
import java.util.concurrent.*;
import java.io.*;
import java.util.*;
import static net.mindview.util.Print.*;
class Sender implements Runnable {
private Random rand = new Random(47);
private PipedWriter out = new PipedWriter();
public PipedWriter getPipedWriter() { return out; }
public void run() {
try {
while(true)
for(char c = ‘A’; c <= ‘z’; c++) {
out.write(c);
TimeUnit.MILLISECONDS.sleep(rand.nextInt(500));
}
} catch(IOException e) {
print(e + " Sender write exception");
} catch(InterruptedException e) {
print(e + " Sender sleep interrupted");
}
}
}
class Receiver implements Runnable {
private PipedReader in;
public Receiver(Sender sender) throws IOException {
in = new PipedReader(sender.getPipedWriter());
}
public void run() {
try {
while(true) {
// Blocks until characters are there:
printnb("Read: " + (char)in.read() + ", ");
}
} catch(IOException e) {
print(e + " Receiver read exception");
}
}
}
public class PipedIO {
public static void main(String[] args) throws Exception {
Sender sender = new Sender();
Receiver receiver = new Receiver(sender);
ExecutorService exec = Executors.newCachedThreadPool();
exec.execute(sender);
exec.execute(receiver);
TimeUnit.SECONDS.sleep(4);
exec.shutdownNow();
}
} /* Output: (65% match)
Read: A, Read: B, Read: C, Read: D, Read: E, Read: F, Read: G, Read: H,
Read: I, Read: J, Read: K, Read: L, Read: M,
java.lang.InterruptedException: sleep interrupted Sender sleep
interrupted
java.io.InterruptedIOException Receiver read exception
*///:~
```

<!--p896-->
Sender and Receiver represent tasks that need to communicate with each other. Sender creates a PipedWriter, which is a standalone object, but inside Receiver the creation of PipedReader must be associated with a PipedWriter in the constructor. The Sender puts data into the Writer and sleeps for a random amount of time. However, Receiver has Concurrency no sleep( ) or wait( ). But when it does a read( ), the pipe automatically blocks when there is no more data. Notice that the sender and receiver are started in main( ), after the objects are completely constructed. If you don’t start completely constructed objects, the pipe can produce inconsistent behavior on different platforms. (Note that BlockingQueues are more robust and easier to use.) An important difference between a PipedReader and normal I/O is seen when shutdownNow( ) is called—the PipedReader is interruptible, whereas if you changed, for example, the in.read( ) call to System.in.read( ), the interrupt( ) would fail to break out of the read( ) call. Exercise 30:(1) Modify PipedIO.java to use a BlockingQueue instead of a pipe. Deadlock Now you understand an object can have synchronized methods or other forms of locking that prevent tasks from accessing that object until the mutex is released. You’ve also learned that tasks can become blocked. Thus it’s possible for one task to get stuck waiting for another task, which in turn waits for another task, and so on, until the chain leads back to a task waiting on the first one. You get a continuous loop of tasks waiting on each other, and no one can move. This is called deadlock.21 If you try running a program and it deadlocks right away, you can immediately track down the bug. The real problem is when your program seems to be working fine but has the hidden potential to deadlock. In this case, you may get no indication that deadlocking is a possibility, so the flaw will be latent in your program until it unexpectedly happens to a customer (in a way that will almost certainly be difficult to reproduce). Thus, preventing deadlock through careful program design is a critical part of developing concurrent systems. The dining philosophers problem, invented by Edsger Dijkstra, is the classic demonstration of deadlock. The basic description specifies five philosophers (but the example shown here will allow any number). These philosophers spend part of their time thinking and part of their time eating. While they are thinking, they don’t need any shared resources, but they eat using a limited number of utensils. In the original problem description, the utensils are forks, and two forks are required to get spaghetti from a bowl in the middle of the table, but it seems to make more sense to say that the utensils are chopsticks. Clearly, each philosopher will require two chopsticks in order to eat. A difficulty is introduced into the problem: As philosophers, they have very little money, so they can only afford five chopsticks (more generally, the same number of chopsticks as philosophers). These are spaced around the table between them. When a philosopher wants to eat, that philosopher must pick up the chopstick to the left and the one to the right. If the philosopher on either side is using a desired chopstick, our philosopher must wait until the necessary chopsticks become available.
```java
//: concurrency/Chopstick.java
// Chopsticks for dining philosophers.
public class Chopstick {
private boolean taken = false;
public synchronized
void take() throws InterruptedException {
```

<!--p897-->
21 You can also have livelock when two tasks are able to change their state (they don’t block) but they never make any useful progress.
```java
while(taken)
wait();
taken = true;
}
public synchronized void drop() {
taken = false;
notifyAll();
}
} ///:~
```
No two Philosopherscan successfully take( ) the same Chopstick at the same time. In addition, if the Chopstick has already been taken by one Philosopher, another can wait( ) until the Chopstick becomes available when the current holder calls drop( ). When a Philosopher task calls take( ), that Philosopher waits until the taken flag is false (until the Philosopher currently holding the Chopstick releases it). Then the task sets the taken flag to true to indicate that the new Philosopher now holds the Chopstick. When this Philosopher is finished with the Chopstick, it calls drop( ) to change the flag and notifyAll( ) any other Philosophers that may be wait( )ingfor the Chopstick.
```java
//: concurrency/Philosopher.java
// A dining philosopher
import java.util.concurrent.*;
import java.util.*;
import static net.mindview.util.Print.*;
public class Philosopher implements Runnable {
private Chopstick left;
private Chopstick right;
private final int id;
private final int ponderFactor;
private Random rand = new Random(47);
private void pause() throws InterruptedException {
if(ponderFactor == 0) return;
TimeUnit.MILLISECONDS.sleep(
rand.nextInt(ponderFactor * 250));
}
public Philosopher(Chopstick left, Chopstick right,
int ident, int ponder) {
this.left = left;
this.right = right;
id = ident;
ponderFactor = ponder;
}
public void run() {
try {
while(!Thread.interrupted()) {
print(this + " " + "thinking");
pause();
// Philosopher becomes hungry
print(this + " " + "grabbing right");
right.take();
print(this + " " + "grabbing left");
left.take();
print(this + " " + "eating");
pause();
right.drop();
left.drop();
}
} catch(InterruptedException e) {
print(this + " " + "exiting via interrupt");
}
```

<!--p898-->
Concurrency
```java
}
public String toString() { return "Philosopher " + id; }
} ///:~
```
In Philosopher.run( ), each Philosopher just thinks and eats continuously. The pause( ) method sleeps( ) for a random period if the ponderFactor is nonzero. Using this, you see the Philosopher thinking for a randomized amount of time, then trying to take( ) the right and left Chopsticks, eating for a randomized amount of time, and then doing it again. Now we can set up a version of the program that will deadlock:
```java
//: concurrency/DeadlockingDiningPhilosophers.java
// Demonstrates how deadlock can be hidden in a program.
// {Args: 0 5 timeout}
import java.util.concurrent.*;
public class DeadlockingDiningPhilosophers {
public static void main(String[] args) throws Exception {
int ponder = 5;
if(args.length > 0)
ponder = Integer.parseInt(args[0]);
int size = 5;
if(args.length > 1)
size = Integer.parseInt(args[1]);
ExecutorService exec = Executors.newCachedThreadPool();
Chopstick[] sticks = new Chopstick[size];
for(int i = 0; i < size; i++)
sticks[i] = new Chopstick();
for(int i = 0; i < size; i++)
exec.execute(new Philosopher(
sticks[i], sticks[(i+1) % size], i, ponder));
if(args.length == 3 && args[2].equals("timeout"))
TimeUnit.SECONDS.sleep(5);
else {
System.out.println("Press ‘Enter’ to quit");
System.in.read();
}
exec.shutdownNow();
}
} /* (Execute to see output) *///:~
```

<!--p899-->
You will observe that if the Philosophersspend very little time thinking, they will all be competing for the Chopstickswhile they try to eat, and deadlock will happen much more quickly. The first command-line argument adjusts the ponder factor, to affect the amount of time each Philosopher spends thinking. If you have lots of Philosophers or they spend a lot of time thinking, you may never see deadlock even though it remains a possibility. A command- line argument of zero tends to make the program deadlock fairly quickly. Note that the Chopstick objects do not need internal identifiers; they are identified by their position in the array sticks. Each Philosopher constructor is given a reference to a left and right Chopstick object. Every Philosopher except the last one is initialized by situating that Philosopher between the next pair of Chopstick objects. The last Philosopher is given the zeroth Chopstick for its right Chopstick, so the round table is completed. That’s because the last Philosopher is sitting right next to the first one, and they both share that zeroth Chopstick. Now it’s possible for all the Philosophersto be trying to eat, waiting on the Philosopher next to them to put down its Chopstick. This will make the program deadlock. If your Philosophers are spending more time thinking than eating, then they have a much lower probability of requiring the shared resources (Chopsticks), and thus you can convince yourself that the program is deadlock free (using a nonzero ponder value, or a large number of Philosophers), even though it isn’t. This example is interesting precisely because it demonstrates that a program can appear to run correctly but actually be able to deadlock. To repair the problem, you must understand that deadlock can occur if four conditions are simultaneously met: 1.Mutual exclusion. At least one resource used by the tasks must not be shareable. In this case, a Chopstick can be used by only one Philosopher at a time. 2.At least one task must be holding a resource and waiting to acquire a resource currently held by another task. That is, for deadlock to occur, a Philosopher must be holding one Chopstick and waiting for another one. 3.A resource cannot be preemptively taken away from a task. Tasks only release resources as a normal event. Our Philosophersare polite and they don’t grab Chopsticksfrom other Philosophers. 4.A circular wait can happen, whereby a task waits on a resource held by another task, which in turn is waiting on a resource held by another task, and so on, until one of the tasks is waiting on a resource held by the first task, thus gridlocking everything. In DeadlockingDiningPhilosophers.java, the circular wait happens because each Philosopher tries to get the right Chopstick first and then the left. Because all these conditions must be met to cause deadlock, you only need to prevent one of them from occurring to prohibit deadlock. In this program, the easiest way to prevent deadlock is to break the fourth condition. This condition happens because each Philosopher is trying to pick up its Chopsticksin a particular sequence: first right, then left. Because of that, it’s possible to get into a situation where each of them is holding its right Chopstick and waiting to get the left, causing the circular wait condition. However, if the last Philosopher is initialized to try to get the left chopstick first and then the right, that Philosopher will never prevent the Philosopher on the immediate right from picking up their its chopstick. In this case, the circular wait is prevented. This is only one solution to the problem, but you could also solve it by preventing one of the other conditions (see advanced threading books for more details):
```java
//: concurrency/FixedDiningPhilosophers.java
// Dining philosophers without deadlock.
// {Args: 5 5 timeout}
import java.util.concurrent.*;
public class FixedDiningPhilosophers {
public static void main(String[] args) throws Exception {
int ponder = 5;
if(args.length > 0)
ponder = Integer.parseInt(args[0]);
int size = 5;
if(args.length > 1)
size = Integer.parseInt(args[1]);
ExecutorService exec = Executors.newCachedThreadPool();
Chopstick[] sticks = new Chopstick[size];
for(int i = 0; i < size; i++)
sticks[i] = new Chopstick();
for(int i = 0; i < size; i++)
if(i < (size-1))
exec.execute(new Philosopher(
sticks[i], sticks[i+1], i, ponder));
else
```

<!--p900-->
Concurrency
```java
exec.execute(new Philosopher(
sticks[0], sticks[i], i, ponder));
if(args.length == 3 && args[2].equals("timeout"))
TimeUnit.SECONDS.sleep(5);
else {
System.out.println("Press ‘Enter’ to quit");
System.in.read();
}
exec.shutdownNow();
}
} /* (Execute to see output) *///:~
```

<!--p901-->
By ensuring that the last Philosopher picks up and puts down the left Chopstick before the right, we remove the deadlock, and the program will run smoothly. There is no language support to help prevent deadlock; it’s up to you to avoid it by careful design. These are not comforting words to the person who’s trying to debug a deadlocking program. Exercise 31:(8) Change DeadlockingDiningPhilosophers.java so that when a philosopher is done with its chopsticks, it drops them into a bin. When a philosopher wants to eat, it takes the next two available chopsticks from the bin. Does this eliminate the possibility of deadlock? Can you reintroduce deadlock by simply reducing the number of available chopsticks? New library components The java.util.concurrent library in Java SE5 introduces a significant number of new classes designed to solve concurrency problems. Learning to use these can help you produce simpler and more robust concurrent programs. This section includes a representative set of examples of various components, but a few of the components—ones that you may be less likely to use and encounter—are not discussed here. Because these components solve various problems, there is no clear way to organize them, so I shall attempt to start with simpler examples and proceed through examples of increasing complexity.
## CountDownLatch
This is used to synchronize one or more tasks by forcing them to wait for the completion of a set of operations being performed by other tasks. You give an initial count to a CountDownLatch object, and any task that calls await( ) on that object will block until the count reaches zero. Other tasks may call countDown( ) on the object to reduce the count, presumably when a task finishes its job. A CountDownLatch is designed to be used in a one-shot fashion; the count cannot be reset. If you need a version that resets the count, you can use a CyclicBarrier instead. The tasks that call countDown( ) are not blocked when they make that call. Only the call to await( ) is blocked until the count reaches zero. A typical use is to divide a problem into n independently solvable tasks and create a CountDownLatch with a value of n. When each task is finished it calls countDown( ) on the latch. Tasks waiting for the problem to be solved call await( ) on the latch to hold themselves back until it is completed. Here’s a skeleton example that demonstrates this technique:
```java
//: concurrency/CountDownLatchDemo.java
import java.util.concurrent.*;
import java.util.*;
import static net.mindview.util.Print.*;
// Performs some portion of a task:
class TaskPortion implements Runnable {
private static int counter = 0;
private final int id = counter++;
private static Random rand = new Random(47);
private final CountDownLatch latch;
TaskPortion(CountDownLatch latch) {
this.latch = latch;
}
public void run() {
try {
doWork();
latch.countDown();
} catch(InterruptedException ex) {
// Acceptable way to exit
}
}
public void doWork() throws InterruptedException {
TimeUnit.MILLISECONDS.sleep(rand.nextInt(2000));
```

<!--p902-->
Concurrency
```java
print(this + "completed");
}
public String toString() {
return String.format("%1$-3d ", id);
}
}
// Waits on the CountDownLatch:
class WaitingTask implements Runnable {
private static int counter = 0;
private final int id = counter++;
private final CountDownLatch latch;
WaitingTask(CountDownLatch latch) {
this.latch = latch;
}
public void run() {
try {
latch.await();
print("Latch barrier passed for " + this);
} catch(InterruptedException ex) {
print(this + " interrupted");
}
}
public String toString() {
return String.format("WaitingTask %1$-3d ", id);
}
}
public class CountDownLatchDemo {
static final int SIZE = 100;
public static void main(String[] args) throws Exception {
ExecutorService exec = Executors.newCachedThreadPool();
// All must share a single CountDownLatch object:
CountDownLatch latch = new CountDownLatch(SIZE);
for(int i = 0; i < 10; i++)
exec.execute(new WaitingTask(latch));
for(int i = 0; i < SIZE; i++)
exec.execute(new TaskPortion(latch));
print("Launched all tasks");
exec.shutdown(); // Quit when all tasks complete
}
} /* (Execute to see output) *///:~
```

<!--p903-->
TaskPortion sleeps for a random period to simulate the completion of part of the task, and WaitingTask indicates a part of the system that must wait until the initial portion of the problem is complete. All tasks work with the same single CountDownLatch, which is defined in main( ). Exercise 32: (7) Use a CountDownLatch to solve the problem of correlating the results from the Entrances in OrnamentalGarden.java. Remove the unnecessary code from the new version of the example. Library thread safety Notice that TaskPortion contains a static Random object, which means that multiple tasks may be calling Random.nextInt( ) at the same time. Is this safe? If there is a problem, it can be solved in this case by giving TaskPortion its own Random object—that is, by removing the static specifier. But the question remains for Java standard library methods in general: Which ones are thread-safe and which ones aren’t? Concurrency Unfortunately, the JDK documentation is not forthcoming on this point. It happens that Random.nextInt( ) is thread-safe, but alas, you shall have to discover this on a case-by- case basis, using either a Web search or by inspecting the Java library code. This is not a particularly good situation for a programming language that was, at least in theory, designed to support concurrency.
## CyclicBarrier
A CyclicBarrier is used in situations where you want to create a group of tasks to perform work in parallel, and then wait until they are all finished before moving on to the next step (something like join( ), it would seem). It brings all the parallel tasks into alignment at the barrier so you can move forward in unison. This is very similar to the CountDownLatch, except that a CountDownLatch is a one-shot event, whereas a CyclicBarrier can be reused over and over. I’ve been fascinated with simulations from the beginning of my experience with computers, and concurrency is a key factor of making simulations possible. The very first program that I can remember writing22was a simulation: a horse-racing game written in BASIC called (because of the file name limitations) HOSRAC.BAS. Here is the object-oriented, threaded version of that program, utilizing a CyclicBarrier:
```java
//: concurrency/HorseRace.java
// Using CyclicBarriers.
import java.util.concurrent.*;
import java.util.*;
import static net.mindview.util.Print.*;
class Horse implements Runnable {
private static int counter = 0;
private final int id = counter++;
private int strides = 0;
private static Random rand = new Random(47);
private static CyclicBarrier barrier;
public Horse(CyclicBarrier b) { barrier = b; }
public synchronized int getStrides() { return strides; }
public void run() {
try {
while(!Thread.interrupted()) {
synchronized(this) {
strides += rand.nextInt(3); // Produces 0, 1 or 2
}
barrier.await();
}
} catch(InterruptedException e) {
// A legitimate way to exit
} catch(BrokenBarrierException e) {
// This one we want to know about
throw new RuntimeException(e);
}
}
public String toString() { return "Horse " + id + " "; }
public String tracks() {
StringBuilder s = new StringBuilder();
for(int i = 0; i < getStrides(); i++)
s.append("*");
s.append(id);
return s.toString();
```

<!--p904-->
22 As a freshman in high school; the classroom had an ASR-33 teletype with a 110-baud acoustic-coupler modem accessing an HP-1000.
```java
}
}
public class HorseRace {
static final int FINISH_LINE = 75;
private List<Horse> horses = new ArrayList<Horse>();
private ExecutorService exec =
Executors.newCachedThreadPool();
private CyclicBarrier barrier;
public HorseRace(int nHorses, final int pause) {
barrier = new CyclicBarrier(nHorses, new Runnable() {
public void run() {
StringBuilder s = new StringBuilder();
for(int i = 0; i < FINISH_LINE; i++)
s.append("="); // The fence on the racetrack
print(s);
for(Horse horse : horses)
print(horse.tracks());
for(Horse horse : horses)
if(horse.getStrides() >= FINISH_LINE) {
print(horse + "won!");
exec.shutdownNow();
return;
}
try {
TimeUnit.MILLISECONDS.sleep(pause);
} catch(InterruptedException e) {
print("barrier-action sleep interrupted");
}
}
});
for(int i = 0; i < nHorses; i++) {
Horse horse = new Horse(barrier);
horses.add(horse);
exec.execute(horse);
}
}
public static void main(String[] args) {
int nHorses = 7;
int pause = 200;
if(args.length > 0) { // Optional argument
int n = new Integer(args[0]);
nHorses = n > 0 ? n : nHorses;
}
if(args.length > 1) { // Optional argument
int p = new Integer(args[1]);
pause = p > -1 ? p : pause;
}
new HorseRace(nHorses, pause);
}
} /* (Execute to see output) *///:~
```

<!--p905-->
A CyclicBarrier can be given a "barrier action," which is a Runnable that is automatically executed when the count reaches zero—this is another distinction between CyclicBarrier and CountdownLatch. Here, the barrier action is created as an anonymous class that is handed to the constructor of CyclicBarrier. Itried having each horse print itself, but then the order of display was dependent on the task manager. The CyclicBarrier allows each horse to do whatever it needs to do in order to move forward, and then it has to wait at the barrier until all the other horses have moved forward. When all horses have moved, the CyclicBarrier automatically calls its Runnable barrieraction task to display the horses in order, along with the fence. Once all the tasks have passed the barrier, it is automatically ready for the next round. To give it the effect of very simple animation, make the size of your console window small enough so that only the horses show.
## DelayQueue
This is an unbounded BlockingQueue of objects that implement the Delayed interface. An object can only be taken from the queue when its delay has expired. The queue is sorted so that the object at the head has a delay that has expired for the longest time. If no delay has expired, then there is no head element and poll( ) will return null (because of this, you cannot place null elements in the queue). Here’s an example where the Delayed objects are themselves tasks, and the DelayedTaskConsumer takes the most "urgent" task (the one that has been expired for the longest time) off the queue and runs it. Note that DelayQueue is thus a variation of a priority queue.
```java
//: concurrency/DelayQueueDemo.java
import java.util.concurrent.*;
import java.util.*;
import static java.util.concurrent.TimeUnit.*;
import static net.mindview.util.Print.*;
class DelayedTask implements Runnable, Delayed {
private static int counter = 0;
private final int id = counter++;
private final int delta;
private final long trigger;
protected static List<DelayedTask> sequence =
new ArrayList<DelayedTask>();
public DelayedTask(int delayInMilliseconds) {
delta = delayInMilliseconds;
trigger = System.nanoTime() +
NANOSECONDS.convert(delta, MILLISECONDS);
sequence.add(this);
}
public long getDelay(TimeUnit unit) {
return unit.convert(
trigger - System.nanoTime(), NANOSECONDS);
}
public int compareTo(Delayed arg) {
DelayedTask that = (DelayedTask)arg;
if(trigger < that.trigger) return -1;
if(trigger > that.trigger) return 1;
return 0;
}
public void run() { printnb(this + " "); }
public String toString() {
return String.format("[%1$-4d]", delta) +
" Task " + id;
}
public String summary() {
return "(" + id + ":" + delta + ")";
}
public static class EndSentinel extends DelayedTask {
private ExecutorService exec;
public EndSentinel(int delay, ExecutorService e) {
super(delay);
exec = e;
```

<!--p906-->
Concurrency
```java
}
public void run() {
for(DelayedTask pt : sequence) {
printnb(pt.summary() + " ");
}
print();
print(this + " Calling shutdownNow()");
exec.shutdownNow();
}
}
}
class DelayedTaskConsumer implements Runnable {
private DelayQueue<DelayedTask> q;
public DelayedTaskConsumer(DelayQueue<DelayedTask> q) {
this.q = q;
}
public void run() {
try {
while(!Thread.interrupted())
q.take().run(); // Run task with the current thread
} catch(InterruptedException e) {
// Acceptable way to exit
}
print("Finished DelayedTaskConsumer");
}
}
public class DelayQueueDemo {
public static void main(String[] args) {
Random rand = new Random(47);
ExecutorService exec = Executors.newCachedThreadPool();
DelayQueue<DelayedTask> queue =
new DelayQueue<DelayedTask>();
// Fill with tasks that have random delays:
for(int i = 0; i < 20; i++)
queue.put(new DelayedTask(rand.nextInt(5000)));
// Set the stopping point
queue.add(new DelayedTask.EndSentinel(5000, exec));
exec.execute(new DelayedTaskConsumer(queue));
}
} /* Output:
[128 ] Task 11 [200 ] Task 7 [429 ] Task 5 [520 ] Task 18 [555 ] Task 1
[961 ] Task 4 [998 ] Task 16 [1207] Task 9 [1693] Task 2 [1809] Task 14
[1861] Task 3 [2278] Task 15 [3288] Task 10 [3551] Task 12 [4258] Task 0
[4258] Task 19 [4522] Task 8 [4589] Task 13 [4861] Task 17 [4868] Task 6
(0:4258) (1:555) (2:1693) (3:1861) (4:961) (5:429) (6:4868) (7:200)
(8:4522) (9:1207) (10:3288) (11:128) (12:3551) (13:4589) (14:1809)
(15:2278) (16:998) (17:4861) (18:520) (19:4258) (20:5000)
[5000] Task 20 Calling shutdownNow()
Finished DelayedTaskConsumer
*///:~
```

<!--p907-->
DelayedTask contains a List<DelayedTask> called sequence that preserves the order in which the tasks were created, so that we can see that sorting does in fact take place. The Delayed interface has one method, getDelay( ), which tells how long it is until the delay time expires or how long ago the delay time has expired. This method forces us to use the TimeUnit class because that’s the argument type. This turns out to be a very convenient class because you can easily convert units without doing any calculations. For example, the value of delta is stored in milliseconds, but the Java SE5 method System.nanoTime( ) produces time in nanoseconds. You can convert the value of delta by saying what units it is in and what units you want it to be in, like this:
```java
NANOSECONDS.convert(delta, MILLISECONDS);
```
In getDelay( ), the desired units are passed in as the unit argument, and you use this to convert the time difference from the trigger time to the units requested by the caller, without even knowing what those units are (this is a simple example of the Strategy design pattern, where part of the algorithm is passed in as an argument). For sorting, the Delayed interface also inherits the Comparable interface, so compareTo( ) must be implemented so that it produces a reasonable comparison. toString( ) and summary( ) provide output formatting, and the nested EndSentinel class provides a way to shut everything down by placing it as the last element in the queue. Note that because DelayedTaskConsumer is itself a task, it has its own Thread which it can use to run each task that comes out of the queue. Since the tasks are being performed in queue priority order, there’s no need in this example to start separate threads to run the DelayedTasks. You can see from the output that the order in which the tasks are created has no effect on execution order—instead, the tasks are executed in delay order as expected.
## PriorityBlockingQueue
This is basically a priority queue that has blocking retrieval operations. Here’s an example where the objects in the priority queue are tasks that emerge from the queue in priority order. A PrioritizedTask is given a priority number to provide this order:
```java
//: concurrency/PriorityBlockingQueueDemo.java
import java.util.concurrent.*;
import java.util.*;
import static net.mindview.util.Print.*;
class PrioritizedTask implements
Runnable, Comparable<PrioritizedTask> {
private Random rand = new Random(47);
private static int counter = 0;
private final int id = counter++;
private final int priority;
protected static List<PrioritizedTask> sequence =
new ArrayList<PrioritizedTask>();
public PrioritizedTask(int priority) {
this.priority = priority;
sequence.add(this);
}
public int compareTo(PrioritizedTask arg) {
return priority < arg.priority ? 1 :
(priority > arg.priority ? -1 : 0);
}
public void run() {
try {
TimeUnit.MILLISECONDS.sleep(rand.nextInt(250));
} catch(InterruptedException e) {
// Acceptable way to exit
}
print(this);
}
public String toString() {
```

<!--p908-->
Concurrency

<!--p909-->
```java
return String.format("[%1$-3d]", priority) +
" Task " + id;
}
public String summary() {
return "(" + id + ":" + priority + ")";
}
public static class EndSentinel extends PrioritizedTask {
private ExecutorService exec;
public EndSentinel(ExecutorService e) {
super(-1); // Lowest priority in this program
exec = e;
}
public void run() {
int count = 0;
for(PrioritizedTask pt : sequence) {
printnb(pt.summary());
if(++count % 5 == 0)
print();
}
print();
print(this + " Calling shutdownNow()");
exec.shutdownNow();
}
}
}
class PrioritizedTaskProducer implements Runnable {
private Random rand = new Random(47);
private Queue<Runnable> queue;
private ExecutorService exec;
public PrioritizedTaskProducer(
Queue<Runnable> q, ExecutorService e) {
queue = q;
exec = e; // Used for EndSentinel
}
public void run() {
// Unbounded queue; never blocks.
// Fill it up fast with random priorities:
for(int i = 0; i < 20; i++) {
queue.add(new PrioritizedTask(rand.nextInt(10)));
Thread.yield();
}
// Trickle in highest-priority jobs:
try {
for(int i = 0; i < 10; i++) {
TimeUnit.MILLISECONDS.sleep(250);
queue.add(new PrioritizedTask(10));
}
// Add jobs, lowest priority first:
for(int i = 0; i < 10; i++)
queue.add(new PrioritizedTask(i));
// A sentinel to stop all the tasks:
queue.add(new PrioritizedTask.EndSentinel(exec));
} catch(InterruptedException e) {
// Acceptable way to exit
}
print("Finished PrioritizedTaskProducer");
}
}
class PrioritizedTaskConsumer implements Runnable {
private PriorityBlockingQueue<Runnable> q;
public PrioritizedTaskConsumer(
PriorityBlockingQueue<Runnable> q) {
this.q = q;
}
public void run() {
try {
while(!Thread.interrupted())
// Use current thread to run the task:
q.take().run();
} catch(InterruptedException e) {
// Acceptable way to exit
}
print("Finished PrioritizedTaskConsumer");
}
}
public class PriorityBlockingQueueDemo {
public static void main(String[] args) throws Exception {
Random rand = new Random(47);
ExecutorService exec = Executors.newCachedThreadPool();
PriorityBlockingQueue<Runnable> queue =
new PriorityBlockingQueue<Runnable>();
exec.execute(new PrioritizedTaskProducer(queue, exec));
exec.execute(new PrioritizedTaskConsumer(queue));
}
} /* (Execute to see output) *///:~
```
As with the previous example, the creation sequence of the PrioritizedTask objects is remembered in the sequence List, for comparison with the actual order of execution. The run( ) method sleeps for a short random time and prints the object information, and the EndSentinel provides the same functionality as before while guaranteeing that it is the last object in the queue. The PrioritizedTaskProducer and PrioritizedTaskConsumer connect to each other through a PriorityBlockingQueue. Because the blocking nature of the queue provides all the necessary synchronization, notice that no explicit synchronization is necessary—you don’t have to think about whether the queue has any elements in it when you’re reading from it, because the queue will simply block the reader when it is out of elements. The greenhouse controller with
## ScheduledExecutor
The Inner Classes chapter introduced the example of a control system applied to a hypothetical greenhouse, turning various facilities on or off or otherwise adjusting them. This can be seen as a kind of concurrency problem, with each desired greenhouse event as a task that is run at a predefined time. The ScheduledThreadPoolExecutor provides just the service necessary to solve the problem. Using either schedule( ) (to run a task once) or scheduleAtFixedRate( ) (to repeat a task at a regular interval), you set up Runnable objects to be executed at some time in the future. Compare the following with the approach used in the Inner Classes chapter to notice how much simpler it is when you can use a predefined tool like ScheduledThreadPoolExecutor:
```java
//: concurrency/GreenhouseScheduler.java
// Rewriting innerclasses/GreenhouseController.java
// to use a ScheduledThreadPoolExecutor.
// {Args: 5000}
import java.util.concurrent.*;
import java.util.*;
public class GreenhouseScheduler {
```

<!--p910-->
Concurrency

<!--p911-->
```java
private volatile boolean light = false;
private volatile boolean water = false;
private String thermostat = "Day";
public synchronized String getThermostat() {
return thermostat;
}
public synchronized void setThermostat(String value) {
thermostat = value;
}
ScheduledThreadPoolExecutor scheduler =
new ScheduledThreadPoolExecutor(10);
public void schedule(Runnable event, long delay) {
scheduler.schedule(event,delay,TimeUnit.MILLISECONDS);
}
public void
repeat(Runnable event, long initialDelay, long period) {
scheduler.scheduleAtFixedRate(
event, initialDelay, period, TimeUnit.MILLISECONDS);
}
class LightOn implements Runnable {
public void run() {
// Put hardware control code here to
// physically turn on the light.
System.out.println("Turning on lights");
light = true;
}
}
class LightOff implements Runnable {
public void run() {
// Put hardware control code here to
// physically turn off the light.
System.out.println("Turning off lights");
light = false;
}
}
class WaterOn implements Runnable {
public void run() {
// Put hardware control code here.
System.out.println("Turning greenhouse water on");
water = true;
}
}
class WaterOff implements Runnable {
public void run() {
// Put hardware control code here.
System.out.println("Turning greenhouse water off");
water = false;
}
}
class ThermostatNight implements Runnable {
public void run() {
// Put hardware control code here.
System.out.println("Thermostat to night setting");
setThermostat("Night");
}
}
class ThermostatDay implements Runnable {
public void run() {
// Put hardware control code here.
System.out.println("Thermostat to day setting");
setThermostat("Day");
}
}
class Bell implements Runnable {
public void run() { System.out.println("Bing!"); }
}
class Terminate implements Runnable {
public void run() {
System.out.println("Terminating");
scheduler.shutdownNow();
// Must start a separate task to do this job,
// since the scheduler has been shut down:
new Thread() {
public void run() {
for(DataPoint d : data)
System.out.println(d);
}
}.start();
}
}
// New feature: data collection
static class DataPoint {
final Calendar time;
final float temperature;
final float humidity;
public DataPoint(Calendar d, float temp, float hum) {
time = d;
temperature = temp;
humidity = hum;
}
public String toString() {
return time.getTime() +
String.format(
" temperature: %1$.1f humidity: %2$.2f",
temperature, humidity);
}
}
private Calendar lastTime = Calendar.getInstance();
{ // Adjust date to the half hour
lastTime.set(Calendar.MINUTE, 30);
lastTime.set(Calendar.SECOND, 00);
}
private float lastTemp = 65.0f;
private int tempDirection = +1;
private float lastHumidity = 50.0f;
private int humidityDirection = +1;
private Random rand = new Random(47);
List<DataPoint> data = Collections.synchronizedList(
new ArrayList<DataPoint>());
class CollectData implements Runnable {
public void run() {
System.out.println("Collecting data");
synchronized(GreenhouseScheduler.this) {
// Pretend the interval is longer than it is:
lastTime.set(Calendar.MINUTE,
lastTime.get(Calendar.MINUTE) + 30);
// One in 5 chances of reversing the direction:
if(rand.nextInt(5) == 4)
tempDirection = -tempDirection;
// Store previous value:
lastTemp = lastTemp +
tempDirection * (1.0f + rand.nextFloat());
if(rand.nextInt(5) == 4)
humidityDirection = -humidityDirection;
lastHumidity = lastHumidity +
humidityDirection * rand.nextFloat();
```

<!--p912-->
Concurrency
```java
// Calendar must be cloned, otherwise all
// DataPoints hold references to the same lastTime.
// For a basic object like Calendar, clone() is OK.
data.add(new DataPoint((Calendar)lastTime.clone(),
lastTemp, lastHumidity));
}
}
}
public static void main(String[] args) {
GreenhouseScheduler gh = new GreenhouseScheduler();
gh.schedule(gh.new Terminate(), 5000);
// Former "Restart" class not necessary:
gh.repeat(gh.new Bell(), 0, 1000);
gh.repeat(gh.new ThermostatNight(), 0, 2000);
gh.repeat(gh.new LightOn(), 0, 200);
gh.repeat(gh.new LightOff(), 0, 400);
gh.repeat(gh.new WaterOn(), 0, 600);
gh.repeat(gh.new WaterOff(), 0, 800);
gh.repeat(gh.new ThermostatDay(), 0, 1400);
gh.repeat(gh.new CollectData(), 500, 500);
}
} /* (Execute to see output) *///:~
```
This version reorganizes the code and adds a new feature: collecting temperature and humidity readings in the greenhouse. A DataPoint holds and displays a single piece of data, while CollectData is the scheduled task that generates simulated data and adds it to the List<DataPoint> in Greenhouse each time it is run. Notice the use of both volatile and synchronized in appropriate places to prevent tasks from interfering with each other. All the methods in the List that holds DataPointsare synchronized using the java.util.Collections utility synchronizedList( ) when the List is created. Exercise 33: (7) Modify GreenhouseScheduler.java so that it uses a DelayQueue instead of a ScheduledExecutor.
## Semaphore
A normal lock (from concurrent.locks or the built-in synchronized lock) only allows one task at a time to access a resource. A counting semaphore allows n tasks to access the resource at the same time. You can also think of a semaphore as handing out "permits" to use a resource, although no actual permit objects are used. As an example, consider the concept of the object pool, which manages a limited number of objects by allowing them to be checked out for use, and then checked back in again when the user is finished. This functionality can be encapsulated in a generic class:

<!--p913-->
```java
//: concurrency/Pool.java
// Using a Semaphore inside a Pool, to restrict
// the number of tasks that can use a resource.
import java.util.concurrent.*;
import java.util.*;
public class Pool<T> {
private int size;
private List<T> items = new ArrayList<T>();
private volatile boolean[] checkedOut;
private Semaphore available;
public Pool(Class<T> classObject, int size) {
this.size = size;
checkedOut = new boolean[size];
available = new Semaphore(size, true);
// Load pool with objects that can be checked out:
for(int i = 0; i < size; ++i)
try {
// Assumes a default constructor:
items.add(classObject.newInstance());
} catch(Exception e) {
throw new RuntimeException(e);
}
}
public T checkOut() throws InterruptedException {
available.acquire();
return getItem();
}
public void checkIn(T x) {
if(releaseItem(x))
available.release();
}
private synchronized T getItem() {
for(int i = 0; i < size; ++i)
if(!checkedOut[i]) {
checkedOut[i] = true;
return items.get(i);
}
return null; // Semaphore prevents reaching here
}
private synchronized boolean releaseItem(T item) {
int index = items.indexOf(item);
if(index == -1) return false; // Not in the list
if(checkedOut[index]) {
checkedOut[index] = false;
return true;
}
return false; // Wasn’t checked out
}
} ///:~
```
In this simplified form, the constructor uses newInstance( ) to load the pool with objects. If you need a new object, you call checkOut( ), and when you’re finished with an object, you hand it to checkIn( ). The boolean checkedOut array keeps track of the objects that are checked out, and is managed by the getItem( ) and releaseItem( ) methods. These, in turn, are guarded by the Semaphore available, so that, in checkOut( ), available blocks the progress of the call if there are no more semaphore permits available (which means there are no more objects in the pool). In checkIn( ), if the object being checked in is valid, a permit is returned to the semaphore. To create an example, we can use Fat, a type of object that is expensive to create because its constructor takes time to run:
```java
//: concurrency/Fat.java
// Objects that are expensive to create.
public class Fat {
private volatile double d; // Prevent optimization
private static int counter = 0;
private final int id = counter++;
public Fat() {
```

<!--p914-->
Concurrency
```java
// Expensive, interruptible operation:
for(int i = 1; i < 10000; i++) {
d += (Math.PI + Math.E) / (double)i;
}
}
public void operation() { System.out.println(this); }
public String toString() { return "Fat id: " + id; }
} ///:~
```
We’ll pool these objects to limit the impact of this constructor. We can test the Pool class by creating a task that will check out Fat objects, hold them for a while, and then check them back in:

<!--p915-->
```java
//: concurrency/SemaphoreDemo.java
// Testing the Pool class
import java.util.concurrent.*;
import java.util.*;
import static net.mindview.util.Print.*;
// A task to check a resource out of a pool:
class CheckoutTask<T> implements Runnable {
private static int counter = 0;
private final int id = counter++;
private Pool<T> pool;
public CheckoutTask(Pool<T> pool) {
this.pool = pool;
}
public void run() {
try {
T item = pool.checkOut();
print(this + "checked out " + item);
TimeUnit.SECONDS.sleep(1);
print(this +"checking in " + item);
pool.checkIn(item);
} catch(InterruptedException e) {
// Acceptable way to terminate
}
}
public String toString() {
return "CheckoutTask " + id + " ";
}
}
public class SemaphoreDemo {
final static int SIZE = 25;
public static void main(String[] args) throws Exception {
final Pool<Fat> pool =
new Pool<Fat>(Fat.class, SIZE);
ExecutorService exec = Executors.newCachedThreadPool();
for(int i = 0; i < SIZE; i++)
exec.execute(new CheckoutTask<Fat>(pool));
print("All CheckoutTasks created");
List<Fat> list = new ArrayList<Fat>();
for(int i = 0; i < SIZE; i++) {
Fat f = pool.checkOut();
printnb(i + ": main() thread checked out ");
f.operation();
list.add(f);
}
Future<?> blocked = exec.submit(new Runnable() {
public void run() {
try {
// Semaphore prevents additional checkout,
// so call is blocked:
pool.checkOut();
} catch(InterruptedException e) {
print("checkOut() Interrupted");
}
}
});
TimeUnit.SECONDS.sleep(2);
blocked.cancel(true); // Break out of blocked call
print("Checking in objects in " + list);
for(Fat f : list)
pool.checkIn(f);
for(Fat f : list)
pool.checkIn(f); // Second checkIn ignored
exec.shutdown();
}
} /* (Execute to see output) *///:~
```
In main( ), a Pool is created to hold Fat objects, and a set of CheckoutTasks begins exercising the Pool. Then the main( ) thread begins checking out Fat objects, and not checking them back in. Once it has checked out all the objects in the pool, no more checkouts will be allowed by the Semaphore. The run( ) method of blocked is thus blocked, and after two seconds the cancel( ) method is called to break out of the Future. Note that redundant checkins are ignored by the Pool. This example relies on the client of the Pool to be rigorous and to voluntarily check items back in, which is the simplest solution when it works. If you cannot always rely on this, Thinking in Patterns (at www.MindView.net) contains further explorations of ways to manage the objects that have been checked out of object pools.
## Exchanger
An Exchanger is a barrier that swaps objects between two tasks. When the tasks enter the barrier, they have one object, and when they leave, they have the object that was formerly held by the other task. Exchangersare typically used when one task is creating objects that are expensive to produce and another task is consuming those objects; this way, more objects can be created at the same time as they are being consumed. To exercise the Exchanger class, we’ll create producer and consumer tasks which, via generics and Generators, will work with any kind of object, and then we’ll apply these to the Fat class. The ExchangerProducer and ExehangerConsumer use a List<T> as the object to be exchanged; each one contains an Exchanger for this List<T>. When you call the Exchanger.exchange( ) method, it blocks until the partner task calls its exchange( ) method, and when both exchange( ) methods have completed, the List<T> has been swapped:
```java
//: concurrency/ExchangerDemo.java
import java.util.concurrent.*;
import java.util.*;
import net.mindview.util.*;
class ExchangerProducer<T> implements Runnable {
private Generator<T> generator;
private Exchanger<List<T>> exchanger;
private List<T> holder;
ExchangerProducer(Exchanger<List<T>> exchg,
Generator<T> gen, List<T> holder) {
exchanger = exchg;
```

<!--p916-->
Concurrency

<!--p917-->
```java
generator = gen;
this.holder = holder;
}
public void run() {
try {
while(!Thread.interrupted()) {
for(int i = 0; i < ExchangerDemo.size; i++)
holder.add(generator.next());
// Exchange full for empty:
holder = exchanger.exchange(holder);
}
} catch(InterruptedException e) {
// OK to terminate this way.
}
}
}
class ExchangerConsumer<T> implements Runnable {
private Exchanger<List<T>> exchanger;
private List<T> holder;
private volatile T value;
ExchangerConsumer(Exchanger<List<T>> ex, List<T> holder){
exchanger = ex;
this.holder = holder;
}
public void run() {
try {
while(!Thread.interrupted()) {
holder = exchanger.exchange(holder);
for(T x : holder) {
value = x; // Fetch out value
holder.remove(x); // OK for CopyOnWriteArrayList
}
}
} catch(InterruptedException e) {
// OK to terminate this way.
}
System.out.println("Final value: " + value);
}
}
public class ExchangerDemo {
static int size = 10;
static int delay = 5; // Seconds
public static void main(String[] args) throws Exception {
if(args.length > 0)
size = new Integer(args[0]);
if(args.length > 1)
delay = new Integer(args[1]);
ExecutorService exec = Executors.newCachedThreadPool();
Exchanger<List<Fat>> xc = new Exchanger<List<Fat>>();
List<Fat>
producerList = new CopyOnWriteArrayList<Fat>(),
consumerList = new CopyOnWriteArrayList<Fat>();
exec.execute(new ExchangerProducer<Fat>(xc,
BasicGenerator.create(Fat.class), producerList));
exec.execute(
new ExchangerConsumer<Fat>(xc,consumerList));
TimeUnit.SECONDS.sleep(delay);
exec.shutdownNow();
}
} /* Output: (Sample)
Final value: Fat id: 29999
*///:~
```

<!--p918-->
In main( ), a single Exchanger is created for both tasks to use, and two CopyOnWriteArrayLists are created for swapping. This particular variant of List can tolerate the remove( ) method being called while the list is being traversed, without throwing a ConcurrentModificationException. The ExchangerProducer fills a List, then swaps the full list for the empty one that the ExchangerConsumer hands it. Because of the Exchanger, the filling of one list and consuming of the other list can happen simultaneously. Exercise 34:(1) Modify ExchangerDemo.java to use your own class instead of Fat. Concurrency Simulation One of the most interesting and exciting uses of concurrency is to create simulations. Using concurrency, each component of a simulation can be its own task, and this makes a simulation much easier to program. Many video games and CGI animations in movies are simulations, and HorseRace.java and GreenhouseScheduler.java, shown earlier, could also be considered simulations. Bank teller simulation This classic simulation can represent any situation where objects appear randomly and require a random amount of time to be served by a limited number of servers. It’s possible to build the simulation to determine the ideal number of servers. In this example, each bank customer requires a certain amount of service time, which is the number of time units that a teller must spend on the customer to serve that customer’s needs. The amount of service time will be different for each customer and will be determined randomly. In addition, you won’t know how many customers will be arriving in each interval, so this will also be determined randomly.

<!--p919-->
```java
//: concurrency/BankTellerSimulation.java
// Using queues and multithreading.
// {Args: 5}
import java.util.concurrent.*;
import java.util.*;
// Read-only objects don’t require synchronization:
class Customer {
private final int serviceTime;
public Customer(int tm) { serviceTime = tm; }
public int getServiceTime() { return serviceTime; }
public String toString() {
return "[" + serviceTime + "]";
}
}
// Teach the customer line to display itself:
class CustomerLine extends ArrayBlockingQueue<Customer> {
public CustomerLine(int maxLineSize) {
super(maxLineSize);
}
public String toString() {
if(this.size() == 0)
return "[Empty]";
StringBuilder result = new StringBuilder();
for(Customer customer : this)
result.append(customer);
return result.toString();
}
}
// Randomly add customers to a queue:
class CustomerGenerator implements Runnable {
private CustomerLine customers;
private static Random rand = new Random(47);
public CustomerGenerator(CustomerLine cq) {
customers = cq;
}
public void run() {
try {
while(!Thread.interrupted()) {
TimeUnit.MILLISECONDS.sleep(rand.nextInt(300));
customers.put(new Customer(rand.nextInt(1000)));
}
} catch(InterruptedException e) {
System.out.println("CustomerGenerator interrupted");
}
System.out.println("CustomerGenerator terminating");
}
}
class Teller implements Runnable, Comparable<Teller> {
private static int counter = 0;
private final int id = counter++;
// Customers served during this shift:
private int customersServed = 0;
private CustomerLine customers;
private boolean servingCustomerLine = true;
public Teller(CustomerLine cq) { customers = cq; }
public void run() {
try {
while(!Thread.interrupted()) {
Customer customer = customers.take();
TimeUnit.MILLISECONDS.sleep(
customer.getServiceTime());
synchronized(this) {
customersServed++;
while(!servingCustomerLine)
wait();
}
}
} catch(InterruptedException e) {
System.out.println(this + "interrupted");
}
System.out.println(this + "terminating");
}
public synchronized void doSomethingElse() {
customersServed = 0;
servingCustomerLine = false;
}
public synchronized void serveCustomerLine() {
assert !servingCustomerLine:"already serving: " + this;
servingCustomerLine = true;
notifyAll();
}
public String toString() { return "Teller " + id + " "; }
public String shortString() { return "T" + id; }
// Used by priority queue:
public synchronized int compareTo(Teller other) {
return customersServed < other.customersServed ? -1 :
(customersServed == other.customersServed ? 0 : 1);
}
}
class TellerManager implements Runnable {
private ExecutorService exec;
private CustomerLine customers;
private PriorityQueue<Teller> workingTellers =
new PriorityQueue<Teller>();
private Queue<Teller> tellersDoingOtherThings =
new LinkedList<Teller>();
private int adjustmentPeriod;
```

<!--p920-->
Concurrency

<!--p921-->
```java
private static Random rand = new Random(47);
public TellerManager(ExecutorService e,
CustomerLine customers, int adjustmentPeriod) {
exec = e;
this.customers = customers;
this.adjustmentPeriod = adjustmentPeriod;
// Start with a single teller:
Teller teller = new Teller(customers);
exec.execute(teller);
workingTellers.add(teller);
}
public void adjustTellerNumber() {
// This is actually a control system. By adjusting
// the numbers, you can reveal stability issues in
// the control mechanism.
// If line is too long, add another teller:
if(customers.size() / workingTellers.size() > 2) {
// If tellers are on break or doing
// another job, bring one back:
if(tellersDoingOtherThings.size() > 0) {
Teller teller = tellersDoingOtherThings.remove();
teller.serveCustomerLine();
workingTellers.offer(teller);
return;
}
// Else create (hire) a new teller
Teller teller = new Teller(customers);
exec.execute(teller);
workingTellers.add(teller);
return;
}
// If line is short enough, remove a teller:
if(workingTellers.size() > 1 &&
customers.size() / workingTellers.size() < 2)
reassignOneTeller();
// If there is no line, we only need one teller:
if(customers.size() == 0)
while(workingTellers.size() > 1)
reassignOneTeller();
}
// Give a teller a different job or a break:
private void reassignOneTeller() {
Teller teller = workingTellers.poll();
teller.doSomethingElse();
tellersDoingOtherThings.offer(teller);
}
public void run() {
try {
while(!Thread.interrupted()) {
TimeUnit.MILLISECONDS.sleep(adjustmentPeriod);
adjustTellerNumber();
System.out.print(customers + " { ");
for(Teller teller : workingTellers)
System.out.print(teller.shortString() + " ");
System.out.println("}");
}
} catch(InterruptedException e) {
System.out.println(this + "interrupted");
}
System.out.println(this + "terminating");
}
public String toString() { return "TellerManager "; }
}
public class BankTellerSimulation {
static final int MAX_LINE_SIZE = 50;
static final int ADJUSTMENT_PERIOD = 1000;
public static void main(String[] args) throws Exception {
ExecutorService exec = Executors.newCachedThreadPool();
// If line is too long, customers will leave:
CustomerLine customers =
new CustomerLine(MAX_LINE_SIZE);
exec.execute(new CustomerGenerator(customers));
// Manager will add and remove tellers as necessary:
exec.execute(new TellerManager(
exec, customers, ADJUSTMENT_PERIOD));
if(args.length > 0) // Optional argument
TimeUnit.SECONDS.sleep(new Integer(args[0]));
else {
System.out.println("Press ‘Enter’ to quit");
System.in.read();
}
exec.shutdownNow();
}
} /* Output: (Sample)
[429][200][207] { T0 T1 }
[861][258][140][322] { T0 T1 }
[575][342][804][826][896][984] { T0 T1 T2 }
[984][810][141][12][689][992][976][368][395][354] { T0 T1 T2 T3 }
Teller 2 interrupted
Teller 2 terminating
Teller 1 interrupted
Teller 1 terminating
TellerManager interrupted
TellerManager terminating
Teller 3 interrupted
Teller 3 terminating
Teller 0 interrupted
Teller 0 terminating
CustomerGenerator interrupted
CustomerGenerator terminating
*///:~
```

<!--p922-->
The Customer objects are very simple, containing only a final int field. Because these objects never change, they are read-only objects and they do not require synchronization or the use of volatile. On top of that, each Teller task only removes one Customer at a time from the input queue, and works on that Customer until it is complete, so a Customer will only be accessed by one task at a time, anyway. CustomerLine represents a single line that the customers wait in before being served by a Teller. This is just an ArrayBlockingQueue that has a toString( ) that prints the results in the desired fashion. A CustomerGenerator is attached to a CustomerLine and puts Customers onto the queue at randomized intervals. A Teller takes Customersoff of the CustomerLine and processes them one at a time, keeping track of the number of Customers it has served during that particular shift. It can be told to doSomethingElse( ) when there aren’t enough customers, and to serveCustomerLine( ) when lots of customers show up. To choose the next teller to put back on the line, the compareTo( ) method looks at the number of customers served so that a PriorityQueue can automatically put the least-worked teller at the forefront. Concurrency The TellerManager is the hub of activity. It keeps track of all the tellers and what’s going on with the customers. One of the interesting things about this simulation is that it attempts to discover the optimum number of tellers for a given customer flow. You can see this in the adjustTellerNumber( ), which is a control system to add and remove tellers in a stable fashion. All control systems have stability issues; if they react too quickly to a change, they are unstable, and if they react too slowly, the system moves to one of its extremes. Exercise 35:(8) Modify BankTellerSimulation.java so that it represents Web clients making requests of a fixed number of servers. The goal is to determine the load that the group of servers can handle. The restaurant simulation This simulation fleshes out the simple Restaurant.java example shown earlier in this chapter by adding more simulation components, such as Orders and Plates, and it reuses the menu classes from the Enumerated Types chapter. It also introduces the Java SE5 SynchronousQueue, which is a blocking queue that has no internal capacity, so each put( ) must wait for a take( ), and vice versa. It’s as if you were handing an object to someone—there’s no table to put it on, so it only works if that person is holding a hand out, ready to receive the object. In this example, the SynchronousQueue represents the place setting in front of a diner, to enforce the idea that only one course can be served at a time. The rest of the classes and functionality of this example either follow from the structure of Restaurant.java or are intended to be a fairly direct mapping from the operations of an actual restaurant:

<!--p923-->
```java
//: concurrency/restaurant2/RestaurantWithQueues.java
// {Args: 5}
package concurrency.restaurant2;
import enumerated.menu.*;
import java.util.concurrent.*;
import java.util.*;
import static net.mindview.util.Print.*;
// This is given to the waiter, who gives it to the chef:
class Order { // (A data-transfer object)
private static int counter = 0;
private final int id = counter++;
private final Customer customer;
private final WaitPerson waitPerson;
private final Food food;
public Order(Customer cust, WaitPerson wp, Food f) {
customer = cust;
waitPerson = wp;
food = f;
}
public Food item() { return food; }
public Customer getCustomer() { return customer; }
public WaitPerson getWaitPerson() { return waitPerson; }
public String toString() {
return "Order: " + id + " item: " + food +
" for: " + customer +
" served by: " + waitPerson;
}
}
// This is what comes back from the chef:
class Plate {
private final Order order;
private final Food food;
public Plate(Order ord, Food f) {
order = ord;
food = f;
}
public Order getOrder() { return order; }
public Food getFood() { return food; }
public String toString() { return food.toString(); }
}
class Customer implements Runnable {
private static int counter = 0;
private final int id = counter++;
private final WaitPerson waitPerson;
// Only one course at a time can be received:
private SynchronousQueue<Plate> placeSetting =
new SynchronousQueue<Plate>();
public Customer(WaitPerson w) { waitPerson = w; }
public void
deliver(Plate p) throws InterruptedException {
// Only blocks if customer is still
// eating the previous course:
placeSetting.put(p);
}
public void run() {
for(Course course : Course.values()) {
Food food = course.randomSelection();
try {
waitPerson.placeOrder(this, food);
// Blocks until course has been delivered:
print(this + "eating " + placeSetting.take());
} catch(InterruptedException e) {
print(this + "waiting for " +
course + " interrupted");
break;
}
}
print(this + "finished meal, leaving");
}
public String toString() {
return "Customer " + id + " ";
}
}
class WaitPerson implements Runnable {
private static int counter = 0;
private final int id = counter++;
private final Restaurant restaurant;
BlockingQueue<Plate> filledOrders =
new LinkedBlockingQueue<Plate>();
public WaitPerson(Restaurant rest) { restaurant = rest; }
public void placeOrder(Customer cust, Food food) {
try {
// Shouldn’t actually block because this is
// a LinkedBlockingQueue with no size limit:
restaurant.orders.put(new Order(cust, this, food));
} catch(InterruptedException e) {
print(this + " placeOrder interrupted");
}
}
public void run() {
```

<!--p924-->
Concurrency

<!--p925-->
```java
try {
while(!Thread.interrupted()) {
// Blocks until a course is ready
Plate plate = filledOrders.take();
print(this + "received " + plate +
" delivering to " +
plate.getOrder().getCustomer());
plate.getOrder().getCustomer().deliver(plate);
}
} catch(InterruptedException e) {
print(this + " interrupted");
}
print(this + " off duty");
}
public String toString() {
return "WaitPerson " + id + " ";
}
}
class Chef implements Runnable {
private static int counter = 0;
private final int id = counter++;
private final Restaurant restaurant;
private static Random rand = new Random(47);
public Chef(Restaurant rest) { restaurant = rest; }
public void run() {
try {
while(!Thread.interrupted()) {
// Blocks until an order appears:
Order order = restaurant.orders.take();
Food requestedItem = order.item();
// Time to prepare order:
TimeUnit.MILLISECONDS.sleep(rand.nextInt(500));
Plate plate = new Plate(order, requestedItem);
order.getWaitPerson().filledOrders.put(plate);
}
} catch(InterruptedException e) {
print(this + " interrupted");
}
print(this + " off duty");
}
public String toString() { return "Chef " + id + " "; }
}
class Restaurant implements Runnable {
private List<WaitPerson> waitPersons =
new ArrayList<WaitPerson>();
private List<Chef> chefs = new ArrayList<Chef>();
private ExecutorService exec;
private static Random rand = new Random(47);
BlockingQueue<Order>
orders = new LinkedBlockingQueue<Order>();
public Restaurant(ExecutorService e, int nWaitPersons,
int nChefs) {
exec = e;
for(int i = 0; i < nWaitPersons; i++) {
WaitPerson waitPerson = new WaitPerson(this);
waitPersons.add(waitPerson);
exec.execute(waitPerson);
}
for(int i = 0; i < nChefs; i++) {
Chef chef = new Chef(this);
chefs.add(chef);
exec.execute(chef);
}
}
public void run() {
try {
while(!Thread.interrupted()) {
// A new customer arrives; assign a WaitPerson:
WaitPerson wp = waitPersons.get(
rand.nextInt(waitPersons.size()));
Customer c = new Customer(wp);
exec.execute(c);
TimeUnit.MILLISECONDS.sleep(100);
}
} catch(InterruptedException e) {
print("Restaurant interrupted");
}
print("Restaurant closing");
}
}
public class RestaurantWithQueues {
public static void main(String[] args) throws Exception {
ExecutorService exec = Executors.newCachedThreadPool();
Restaurant restaurant = new Restaurant(exec, 5, 2);
exec.execute(restaurant);
if(args.length > 0) // Optional argument
TimeUnit.SECONDS.sleep(new Integer(args[0]));
else {
print("Press ‘Enter’ to quit");
System.in.read();
}
exec.shutdownNow();
}
} /* Output: (Sample)
WaitPerson 0 received SPRING_ROLLS delivering to Customer 1
Customer 1 eating SPRING_ROLLS
WaitPerson 3 received SPRING_ROLLS delivering to Customer 0
Customer 0 eating SPRING_ROLLS
WaitPerson 0 received BURRITO delivering to Customer 1
Customer 1 eating BURRITO
WaitPerson 3 received SPRING_ROLLS delivering to Customer 2
Customer 2 eating SPRING_ROLLS
WaitPerson 1 received SOUP delivering to Customer 3
Customer 3 eating SOUP
WaitPerson 3 received VINDALOO delivering to Customer 0
Customer 0 eating VINDALOO
WaitPerson 0 received FRUIT delivering to Customer 1
...
*///:~
```

<!--p926-->
One very important thing to observe about this example is the management of complexity using queues to communicate between tasks. This single technique greatly simplifies the process of concurrent programming by inverting the control: The tasks do not directly interfere with each other. Instead, the tasks send objects to each other via queues. The receiving task handles the object, treating it as a message rather than having the message inflicted upon it. If you follow this technique whenever you can, you stand a much better chance of building robust concurrent systems. Exercise 36:(10) Modify RestaurantWithQueues.java so there’s one OrderTicket object per table. Change order to orderTicket, and add a Table class, with multiple Customersper table. Concurrency Distributing work Here’s a simulation example that brings together many of the concepts in this chapter. Consider a hypothetical robotic assembly line for automobiles. Each Car will be built in several stages, starting with chassis creation, followed by the attachment of the engine, drive train, and wheels.

<!--p927-->
```java
//: concurrency/CarBuilder.java
// A complex example of tasks working together.
import java.util.concurrent.*;
import java.util.*;
import static net.mindview.util.Print.*;
class Car {
private final int id;
private boolean
engine = false, driveTrain = false, wheels = false;
public Car(int idn) { id = idn; }
// Empty Car object:
public Car() { id = -1; }
public synchronized int getId() { return id; }
public synchronized void addEngine() { engine = true; }
public synchronized void addDriveTrain() {
driveTrain = true;
}
public synchronized void addWheels() { wheels = true; }
public synchronized String toString() {
return "Car " + id + " [" + " engine: " + engine
+ " driveTrain: " + driveTrain
+ " wheels: " + wheels + " ]";
}
}
class CarQueue extends LinkedBlockingQueue<Car> {}
class ChassisBuilder implements Runnable {
private CarQueue carQueue;
private int counter = 0;
public ChassisBuilder(CarQueue cq) { carQueue = cq; }
public void run() {
try {
while(!Thread.interrupted()) {
TimeUnit.MILLISECONDS.sleep(500);
// Make chassis:
Car c = new Car(counter++);
print("ChassisBuilder created " + c);
// Insert into queue
carQueue.put(c);
}
} catch(InterruptedException e) {
print("Interrupted: ChassisBuilder");
}
print("ChassisBuilder off");
}
}
class Assembler implements Runnable {
private CarQueue chassisQueue, finishingQueue;
private Car car;
private CyclicBarrier barrier = new CyclicBarrier(4);
private RobotPool robotPool;
public Assembler(CarQueue cq, CarQueue fq, RobotPool rp){
chassisQueue = cq;
finishingQueue = fq;
robotPool = rp;
}
public Car car() { return car; }
public CyclicBarrier barrier() { return barrier; }
public void run() {
try {
while(!Thread.interrupted()) {
// Blocks until chassis is available:
car = chassisQueue.take();
// Hire robots to perform work:
robotPool.hire(EngineRobot.class, this);
robotPool.hire(DriveTrainRobot.class, this);
robotPool.hire(WheelRobot.class, this);
barrier.await(); // Until the robots finish
// Put car into finishingQueue for further work
finishingQueue.put(car);
}
} catch(InterruptedException e) {
print("Exiting Assembler via interrupt");
} catch(BrokenBarrierException e) {
// This one we want to know about
throw new RuntimeException(e);
}
print("Assembler off");
}
}
class Reporter implements Runnable {
private CarQueue carQueue;
public Reporter(CarQueue cq) { carQueue = cq; }
public void run() {
try {
while(!Thread.interrupted()) {
print(carQueue.take());
}
} catch(InterruptedException e) {
print("Exiting Reporter via interrupt");
}
print("Reporter off");
}
}
abstract class Robot implements Runnable {
private RobotPool pool;
public Robot(RobotPool p) { pool = p; }
protected Assembler assembler;
public Robot assignAssembler(Assembler assembler) {
this.assembler = assembler;
return this;
}
private boolean engage = false;
public synchronized void engage() {
engage = true;
notifyAll();
}
// The part of run() that’s different for each robot:
abstract protected void performService();
public void run() {
try {
powerDown(); // Wait until needed
```

<!--p928-->
Concurrency

<!--p929-->
```java
while(!Thread.interrupted()) {
performService();
assembler.barrier().await(); // Synchronize
// We’re done with that job...
powerDown();
}
} catch(InterruptedException e) {
print("Exiting " + this + " via interrupt");
} catch(BrokenBarrierException e) {
// This one we want to know about
throw new RuntimeException(e);
}
print(this + " off");
}
private synchronized void
powerDown() throws InterruptedException {
engage = false;
assembler = null; // Disconnect from the Assembler
// Put ourselves back in the available pool:
pool.release(this);
while(engage == false) // Power down
wait();
}
public String toString() { return getClass().getName(); }
}
class EngineRobot extends Robot {
public EngineRobot(RobotPool pool) { super(pool); }
protected void performService() {
print(this + " installing engine");
assembler.car().addEngine();
}
}
class DriveTrainRobot extends Robot {
public DriveTrainRobot(RobotPool pool) { super(pool); }
protected void performService() {
print(this + " installing DriveTrain");
assembler.car().addDriveTrain();
}
}
class WheelRobot extends Robot {
public WheelRobot(RobotPool pool) { super(pool); }
protected void performService() {
print(this + " installing Wheels");
assembler.car().addWheels();
}
}
class RobotPool {
// Quietly prevents identical entries:
private Set<Robot> pool = new HashSet<Robot>();
public synchronized void add(Robot r) {
pool.add(r);
notifyAll();
}
public synchronized void
hire(Class<? extends Robot> robotType, Assembler d)
throws InterruptedException {
for(Robot r : pool)
if(r.getClass().equals(robotType)) {
pool.remove(r);
r.assignAssembler(d);
r.engage(); // Power it up to do the task
return;
}
wait(); // None available
hire(robotType, d); // Try again, recursively
}
public synchronized void release(Robot r) { add(r); }
}
public class CarBuilder {
public static void main(String[] args) throws Exception {
CarQueue chassisQueue = new CarQueue(),
finishingQueue = new CarQueue();
ExecutorService exec = Executors.newCachedThreadPool();
RobotPool robotPool = new RobotPool();
exec.execute(new EngineRobot(robotPool));
exec.execute(new DriveTrainRobot(robotPool));
exec.execute(new WheelRobot(robotPool));
exec.execute(new Assembler(
chassisQueue, finishingQueue, robotPool));
exec.execute(new Reporter(finishingQueue));
// Start everything running by producing chassis:
exec.execute(new ChassisBuilder(chassisQueue));
TimeUnit.SECONDS.sleep(7);
exec.shutdownNow();
}
} /* (Execute to see output) *///:~
```

<!--p930-->

<!--p931-->
The Carsare transported from one place to another via a CarQueue, which is a type of LinkedBlockingQueue. A ChassisBuilder creates an unadorned Car and places it on a CarQueue. The Assembler takes the Car off a CarQueue and hires Robotsto work on it. A CyclicBarrier allows the Assembler to wait until all the Robots are finished, at which time it puts the Car onto the outgoing CarQueue to be transported to the next operation. The consumer of the final CarQueue isa Reporter object, which just prints the Car to show that the tasks have been properly completed. The Robotsare managed in a pool, and when work needs to be done, the appropriate Robot is hired from the pool. After the work is completed, the Robot returns to the pool. In main( ), all the necessary objects are created and the tasks are initialized, with the ChassisBuilder begun last to start the process. (However, because of the behavior of the LinkedBlockingQueue, it wouldn’t matter if it were started first.) Note that this program follows all the guidelines regarding object and task lifetime presented in this chapter, and so the shutdown process is safe. You’ll notice that Car has all of its methods synchronized. As it turns out, in this example this is redundant, because within the factory the Cars move through the queues and only one task can work on a car at a time. Basically, the queues force serialized access to the Cars. But this is exactly the kind of trap you can fall into—you can say "Let’s try to optimize by not synchronizing the Car class because it doesn’t look like it needs it here." But later, when this system is connected to another which does need the Car to be synchronized, it breaks. Brian Goetz comments: It’s much easier to say, "Car might be used from multiple threads, so let’s make it thread-safe in the obvious way." The way I characterize this approach is: At public parks, you will find guard rails where there is a steep drop, and you may find signs that say, "Don’t lean on the guard rail." Of course, the real purpose of this rule is not to Concurrency prevent you from leaning on the rail—it is to prevent you from falling off the cliff. But "Don’t lean on the rail" is a much easier rule to follow than "Don’t fall off the cliff" Exercise 37: (2) Modify CarBuilder.java to add another stage to the car-building process, whereby you add the exhaust system, body, and fenders. As with the second stage, assume these processes can be performed simultaneously by robots. Exercise 38:(3) Using the approach in CarBuilder.java, model the house-building story that was given in this chapter. Performance tuning A significant number of classes in Java SEs’s java.util.concurrent library exist to provide performance improvements. When you peruse the concurrent library, it can be difficult to discern which classes are intended for regular use (such as BlockingQueues) and which ones are only for improving performance. In this section we will look at some of the issues and classes surrounding performance tuning. Comparing mutex technologies Now that Java includes the old synchronized keyword along with the new Java SE5 Lock and Atomic classes, it is interesting to compare the different approaches so that we can understand more about the value of each and where to use them. The naive approach is to try a simple test on each approach, like this:
```java
//: concurrency/SimpleMicroBenchmark.java
// The dangers of microbenchmarking.
import java.util.concurrent.locks.*;
abstract class Incrementable {
protected long counter = 0;
public abstract void increment();
}
class SynchronizingTest extends Incrementable {
public synchronized void increment() { ++counter; }
}
class LockingTest extends Incrementable {
private Lock lock = new ReentrantLock();
public void increment() {
lock.lock();
try {
++counter;
} finally {
lock.unlock();
}
}
}
public class SimpleMicroBenchmark {
static long test(Incrementable incr) {
long start = System.nanoTime();
for(long i = 0; i < 10000000L; i++)
incr.increment();
return System.nanoTime() - start;
}
public static void main(String[] args) {
long synchTime = test(new SynchronizingTest());
long lockTime = test(new LockingTest());
System.out.printf("synchronized: %1$10d\n", synchTime);
System.out.printf("Lock: %1$10d\n", lockTime);
System.out.printf("Lock/synchronized = %1$.3f",
(double)lockTime/(double)synchTime);
}
} /* Output: (75% match)
synchronized: 244919117
Lock: 939098964
```

<!--p932-->
Concurrency
```java
Lock/synchronized = 3.834
*///:~
```
You can see from the output that calls to the synchronized method appear to be faster than using a ReentrantLock. What’s happened here? This example demonstrates the dangers of so-called "microbenchmarking."23 This term generally refers to performance testing a feature in isolation, out of context. Of course, you must still write tests to verify assertions like "Lock is much faster than synchronized."But you need an awareness of what’s really happening during compilation and run time when you write these kinds of tests. There are a number of problems with the above example. First and foremost, we will only see the true performance difference if the mutexes are under contention, so there must be multiple tasks trying to access the mutexed code sections. In the above example, each mutex is tested by the single main( ) thread, in isolation. Secondly, it’s possible that the compiler can perform special optimizations when it sees the synchronized keyword, and perhaps even notice that this program is single-threaded. The compiler might even identify that the counter is simply being incremented a fixed number of times, and just precalculate the result. Different compilers and runtime systems vary, so it’s hard to know exactly what will happen, but we need to prevent the possibility that the compiler can predict the outcome. To create a valid test, we must make the program more complex. First we need multiple tasks, and not just tasks that change internal values, but also tasks that read those values (otherwise the optimizer may recognize that the values are never being used). In addition, the calculation must be complex and unpredictable enough that the compiler will have no chance to perform aggressive optimizations. This will be accomplished by pre-loading a large array of random ints (pre-loading to reduce the impact of calls to Random.nextInt( ) on the main loops) and using those values in a summation:
```java
//: concurrency/SynchronizationComparisons.java
// Comparing the performance of explicit Locks
// and Atomics versus the synchronized keyword.
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import java.util.concurrent.locks.*;
import java.util.*;
import static net.mindview.util.Print.*;
abstract class Accumulator {
public static long cycles = 50000L;
// Number of Modifiers and Readers during each test:
private static final int N = 4;
public static ExecutorService exec =
Executors.newFixedThreadPool(N*2);
private static CyclicBarrier barrier =
new CyclicBarrier(N*2 + 1);
protected volatile int index = 0;
protected volatile long value = 0;
protected long duration = 0;
protected String id = "error";
protected final static int SIZE = 100000;
protected static int[] preLoaded = new int[SIZE];
static {
// Load the array of random numbers:
```

<!--p933-->
23 Brian Goetz was very helpful in explaining these issues to me. See his article at www- 128.ibm.com/developerworks/library/j-jtp12214 for more about performance measurement.
```java
Random rand = new Random(47);
for(int i = 0; i < SIZE; i++)
preLoaded[i] = rand.nextInt();
}
public abstract void accumulate();
public abstract long read();
private class Modifier implements Runnable {
public void run() {
for(long i = 0; i < cycles; i++)
accumulate();
try {
barrier.await();
} catch(Exception e) {
throw new RuntimeException(e);
}
}
}
private class Reader implements Runnable {
private volatile long value;
public void run() {
for(long i = 0; i < cycles; i++)
value = read();
try {
barrier.await();
} catch(Exception e) {
throw new RuntimeException(e);
}
}
}
public void timedTest() {
long start = System.nanoTime();
for(int i = 0; i < N; i++) {
exec.execute(new Modifier());
exec.execute(new Reader());
}
try {
barrier.await();
} catch(Exception e) {
throw new RuntimeException(e);
}
duration = System.nanoTime() - start;
printf("%-13s: %13d\n", id, duration);
}
public static void
report(Accumulator acc1, Accumulator acc2) {
printf("%-22s: %.2f\n", acc1.id + "/" + acc2.id,
(double)acc1.duration/(double)acc2.duration);
}
}
class BaseLine extends Accumulator {
{ id = "BaseLine"; }
public void accumulate() {
value += preLoaded[index++];
if(index >= SIZE) index = 0;
}
public long read() { return value; }
}
class SynchronizedTest extends Accumulator {
{ id = "synchronized"; }
public synchronized void accumulate() {
value += preLoaded[index++];
```

<!--p934-->
Concurrency

<!--p935-->
```java
if(index >= SIZE) index = 0;
}
public synchronized long read() {
return value;
}
}
class LockTest extends Accumulator {
{ id = "Lock"; }
private Lock lock = new ReentrantLock();
public void accumulate() {
lock.lock();
try {
value += preLoaded[index++];
if(index >= SIZE) index = 0;
} finally {
lock.unlock();
}
}
public long read() {
lock.lock();
try {
return value;
} finally {
lock.unlock();
}
}
}
class AtomicTest extends Accumulator {
{ id = "Atomic"; }
private AtomicInteger index = new AtomicInteger(0);
private AtomicLong value = new AtomicLong(0);
public void accumulate() {
// Oops! Relying on more than one Atomic at
// a time doesn’t work. But it still gives us
// a performance indicator:
int i = index.getAndIncrement();
value.getAndAdd(preLoaded[i]);
if(++i >= SIZE)
index.set(0);
}
public long read() { return value.get(); }
}
public class SynchronizationComparisons {
static BaseLine baseLine = new BaseLine();
static SynchronizedTest synch = new SynchronizedTest();
static LockTest lock = new LockTest();
static AtomicTest atomic = new AtomicTest();
static void test() {
print("============================");
printf("%-12s : %13d\n", "Cycles", Accumulator.cycles);
baseLine.timedTest();
synch.timedTest();
lock.timedTest();
atomic.timedTest();
Accumulator.report(synch, baseLine);
Accumulator.report(lock, baseLine);
Accumulator.report(atomic, baseLine);
Accumulator.report(synch, lock);
Accumulator.report(synch, atomic);
Accumulator.report(lock, atomic);
}
public static void main(String[] args) {
int iterations = 5; // Default
if(args.length > 0) // Optionally change iterations
iterations = new Integer(args[0]);
// The first time fills the thread pool:
print("Warmup");
baseLine.timedTest();
// Now the initial test doesn’t include the cost
// of starting the threads for the first time.
// Produce multiple data points:
for(int i = 0; i < iterations; i++) {
test();
Accumulator.cycles *= 2;
}
Accumulator.exec.shutdown();
}
} /* Output: (Sample)
Warmup
BaseLine : 34237033
============================
Cycles : 50000
BaseLine : 20966632
synchronized : 24326555
Lock : 53669950
Atomic : 30552487
synchronized/BaseLine : 1.16
Lock/BaseLine : 2.56
Atomic/BaseLine : 1.46
synchronized/Lock : 0.45
synchronized/Atomic : 0.79
Lock/Atomic : 1.76
============================
Cycles : 100000
BaseLine : 41512818
synchronized : 43843003
Lock : 87430386
Atomic : 51892350
synchronized/BaseLine : 1.06
Lock/BaseLine : 2.11
Atomic/BaseLine : 1.25
synchronized/Lock : 0.50
synchronized/Atomic : 0.84
Lock/Atomic : 1.68
============================
Cycles : 200000
BaseLine : 80176670
synchronized : 5455046661
Lock : 177686829
Atomic : 101789194
synchronized/BaseLine : 68.04
Lock/BaseLine : 2.22
Atomic/BaseLine : 1.27
synchronized/Lock : 30.70
synchronized/Atomic : 53.59
Lock/Atomic : 1.75
============================
Cycles : 400000
BaseLine : 160383513
synchronized : 780052493
Lock : 362187652
Atomic : 202030984
synchronized/BaseLine : 4.86
```

<!--p936-->
Concurrency
```java
Lock/BaseLine : 2.26
Atomic/BaseLine : 1.26
synchronized/Lock : 2.15
synchronized/Atomic : 3.86
Lock/Atomic : 1.79
============================
Cycles : 800000
BaseLine : 322064955
synchronized : 336155014
Lock : 704615531
Atomic : 393231542
synchronized/BaseLine : 1.04
Lock/BaseLine : 2.19
Atomic/BaseLine : 1.22
synchronized/Lock : 0.47
synchronized/Atomic : 0.85
Lock/Atomic : 1.79
============================
Cycles : 1600000
BaseLine : 650004120
synchronized : 52235762925
Lock : 1419602771
Atomic : 796950171
synchronized/BaseLine : 80.36
Lock/BaseLine : 2.18
Atomic/BaseLine : 1.23
synchronized/Lock : 36.80
synchronized/Atomic : 65.54
Lock/Atomic : 1.78
============================
Cycles : 3200000
BaseLine : 1285664519
synchronized : 96336767661
Lock : 2846988654
Atomic : 1590545726
synchronized/BaseLine : 74.93
Lock/BaseLine : 2.21
Atomic/BaseLine : 1.24
synchronized/Lock : 33.84
synchronized/Atomic : 60.57
Lock/Atomic : 1.79
*///:~
```

<!--p937-->

<!--p938-->
This program uses the Template Method design pattern24 to put all the common code in the base class and isolate all the varying code in the derivedclass implementations of accumulate( ) and read( ). In each of the derived classes SynchronizedTest, LockTest, and AtomicTest, you can see how accumulate( ) and read( ) express different ways of implementing mutual exclusion. In this program, tasks are executed via a FixedThreadPool in an attempt to keep all the thread creation at the beginning, and prevent any extra cost during the tests. Just to make sure, the initial test is duplicated and the first result is discarded because it includes the initial thread creation. A CyclicBarrier is necessary because we want to make sure all the tasks have completed before declaring each test complete. A static clause is used to pre-load the array of random numbers, before any tests begin. This way, if there is any overhead to generating random numbers, we won’t see it during the test. 24 See Thinking in Patterns at www.MindView.net. Each time accumulate( ) is called, it moves to the next place in the array preLoaded (wrapping to the beginning of the array) and adds another randomly generated number to value. The multiple Modifier and Reader tasks provide contention on the Accumulator object. Notice that in AtomicTest, I observe that the situation is too complex to try to use Atomic objects—basically, if more than one Atomic object is involved, you will probably be forced to give up and use more conventional mutexes (the JDK documentation specifically states that using Atomic objects only works when the critical updates for an object are confined to a single variable). However, the test is left in place so that you can still get a feel for the performance benefit of Atomic objects. In main( ), the test is run repeatedly and you can decide to ask for more than five repetitions (the default). For each repetition, the number of test cycles is doubled, so you can see how the different mutexes behave when running for longer and longer times. As you can see from the output, the results are rather surprising. For the first four iterations, the synchronized keyword seems to be more efficient than using a Lock or an Atomic. But suddenly, a threshold is crossed and synchronized seems to become quite inefficient, while Lock and Atomic seem to roughly maintain their proportion to the BaseLine test, and therefore become much more efficient than synchronized. Keep in mind that this program only gives an indication of the differences between the various mutex approaches, and the output above only indicates these differences on my particular machine under my particular circumstances. As you can see if you experiment with it, there can be significant shifts in behavior when different numbers of threads are used and when the program is run for longer periods of time. Some hotspot runtime optimizations are not invoked until a program has been running for several minutes, and in the case of server programs, several hours. That said, it is fairly clear that using Lock is usually significantly more efficient than using synchronized, and it also appears that the overhead of synchronized varies widely, while Locksare relatively consistent. Does this mean you should never use the synchronized keyword? There are two factors to consider: First, in SynchronizationComparisons.java, the bodies of the mutexed methods are extremely small. In general, this is a good practice—only mutex the sections that you absolutely must. However, in practice the mutexed sections may be larger than those in the above example, and so the percentage of time in the body will probably be significantly bigger than the overhead of entering and exiting the mutex, and could overwhelm any benefit of speeding up the mutex. Of course, the only way to know is— when you’re tuning for performance, no sooner—to try the different approaches and see what impact they have. Second, it’s clear from reading the code in this chapter that the synchronized keyword produces much more readable code than the lock try/finally-unlockidiom that Locks require, and that’s why this chapter primarily uses the synchronized keyword. As I’ve stated elsewhere in this book, code is read much more than it is written—when programming, it is more important to communicate with other humans than it is to communicate with the computer—and so readability of code is critical. As a result, it makes sense to start with the synchronized keyword and only change to Lock objects when you are tuning for performance. Finally, it’s nice when you can use the Atomic classes in your concurrent program, but be aware that, as we saw in SynchronizationComparisons.java, Atomic objects are only useful in very simple cases, generally when you only have one Atomic object that’s being modified and when that object is independent from all other objects. It’s safer to start with more traditional mutexing approaches and only attempt to change to Atomic later, if performance requirements dictate. Concurrency Lock-free containers As emphasized in the Holding Your Objects chapter, containers are a fundamental tool in all programming, and this includes concurrent programming. For this reason, early containers like Vector and Hashtable had many synchronized methods, which caused unacceptable overhead when they were not being used in multithreaded applications. In Java 1.2, the new containers library was unsynchronized, and the Collections class was given various static "synchronized" decoration methods to synchronize the different types of containers. Although this was an improvement because it gave you a choice about whether you use synchronization with your container, the overhead is still based on synchronized locking. Java SE5 has added new containers specifically to increase thread-safe performance, using clever techniques to eliminate locking. The general strategy behind these lock-free containers is this: Modifications to the containers can happen at the same time that reads are occurring, as long as the readers can only see the results of completed modifications. A modification is performed on a separate copy of a portion of the data structure (or sometimes a copy of the whole thing), and this copy is invisible during the modification process. Only when the modification is complete is the modified structure atomically swapped with the "main" data structure, and after that readers will see the modification. In CopyOnWriteArrayList, a write will cause a copy of the entire underlying array to be created. The original array is left in place so that reads can safely occur while the copied array is being modified. When the modification is complete, an atomic operation swaps the new array in so that new reads will see the new information. One of the benefits of CopyOnWriteArrayList is that it does not throw ConcurrentModificationException when multiple iterators are traversing and modifying the list, so you don’t have to write special code to protect against such exceptions, as you’ve had to do in the past. CopyOnWriteArraySet uses CopyOnWriteArrayList to achieve its lock-free behavior. ConcurrentHashMap and ConcurrentLinkedQueue use similar techniques to allow concurrent reads and writes, but only portions of the container are copied and modified rather than the entire container. However, readers will still not see any modifications before they are complete. ConcurrentHashMap doesn’t throw ConcurrentModificationExceptions. Performance issues As long as you are primarily reading from a lock-free container, it will be much faster than its synchronized counterpart because the overhead of acquiring and releasing locks is eliminated. This is still true for a small number of writes to a lock-free container, but it would be interesting to get an idea of what "small" means. This section will produce a rough idea of the performance differences of these containers under different conditions. I’ll start with a generic framework for performing tests on any type of container, including Maps. The generic parameter C represents the container type:

<!--p939-->
```java
//: concurrency/Tester.java
// Framework to test performance of concurrency containers.
import java.util.concurrent.*;
import net.mindview.util.*;
public abstract class Tester<C> {
static int testReps = 10;
static int testCycles = 1000;
static int containerSize = 1000;
abstract C containerInitializer();
abstract void startReadersAndWriters();
C testContainer;
String testId;
int nReaders;
int nWriters;
volatile long readResult = 0;
volatile long readTime = 0;
volatile long writeTime = 0;
CountDownLatch endLatch;
static ExecutorService exec =
Executors.newCachedThreadPool();
Integer[] writeData;
Tester(String testId, int nReaders, int nWriters) {
this.testId = testId + " " +
nReaders + "r " + nWriters + "w";
this.nReaders = nReaders;
this.nWriters = nWriters;
writeData = Generated.array(Integer.class,
new RandomGenerator.Integer(), containerSize);
for(int i = 0; i < testReps; i++) {
runTest();
readTime = 0;
writeTime = 0;
}
}
void runTest() {
endLatch = new CountDownLatch(nReaders + nWriters);
testContainer = containerInitializer();
startReadersAndWriters();
try {
endLatch.await();
} catch(InterruptedException ex) {
System.out.println("endLatch interrupted");
}
System.out.printf("%-27s %14d %14d\n",
testId, readTime, writeTime);
if(readTime != 0 && writeTime != 0)
System.out.printf("%-27s %14d\n",
"readTime + writeTime =", readTime + writeTime);
}
abstract class TestTask implements Runnable {
abstract void test();
abstract void putResults();
long duration;
public void run() {
long startTime = System.nanoTime();
test();
duration = System.nanoTime() - startTime;
synchronized(Tester.this) {
putResults();
}
endLatch.countDown();
}
}
public static void initMain(String[] args) {
if(args.length > 0)
testReps = new Integer(args[0]);
if(args.length > 1)
testCycles = new Integer(args[1]);
if(args.length > 2)
containerSize = new Integer(args[2]);
System.out.printf("%-27s %14s %14s\n",
```

<!--p940-->
Concurrency
```java
"Type", "Read time", "Write time");
}
} ///:~
```
The abstract method containerInitializer( ) returns the initialized container to be tested, which is stored in the field testContainer. The other abstract method, startReadersAndWriters( ), starts the reader and writer tasks that will read and modify the container under test. Different tests are run with varying number of readers and writers to see the effects of lock contention (for the synchronized containers) and writes (for the lock-free containers). The constructor is given various information about the test (the argument identifiers should be self-explanatory), then it calls the runTest( ) method repetitions times. runTest( ) creates a CountDownLatch (so the test can know when all the tasks are complete), initializes the container, then calls startReadersAndWriters( ) and waits until they all complete. Each "Reader" or "Writer" class is based on TestTask, which measures the duration of its abstract test( ) method, then calls putResults( ) inside a synchronized block to store the results. To use this framework (in which you’ll recognize the Template Method design pattern), we must inherit from Tester for the particular container type we wish to test, and provide appropriate Reader and Writer classes:

<!--p941-->
```java
//: concurrency/ListComparisons.java
// {Args: 1 10 10} (Fast verification check during build)
// Rough comparison of thread-safe List performance.
import java.util.concurrent.*;
import java.util.*;
import net.mindview.util.*;
abstract class ListTest extends Tester<List<Integer>> {
ListTest(String testId, int nReaders, int nWriters) {
super(testId, nReaders, nWriters);
}
class Reader extends TestTask {
long result = 0;
void test() {
for(long i = 0; i < testCycles; i++)
for(int index = 0; index < containerSize; index++)
result += testContainer.get(index);
}
void putResults() {
readResult += result;
readTime += duration;
}
}
class Writer extends TestTask {
void test() {
for(long i = 0; i < testCycles; i++)
for(int index = 0; index < containerSize; index++)
testContainer.set(index, writeData[index]);
}
void putResults() {
writeTime += duration;
}
}
void startReadersAndWriters() {
for(int i = 0; i < nReaders; i++)
exec.execute(new Reader());
for(int i = 0; i < nWriters; i++)
exec.execute(new Writer());
}
}
class SynchronizedArrayListTest extends ListTest {
List<Integer> containerInitializer() {
return Collections.synchronizedList(
new ArrayList<Integer>(
new CountingIntegerList(containerSize)));
}
SynchronizedArrayListTest(int nReaders, int nWriters) {
super("Synched ArrayList", nReaders, nWriters);
}
}
class CopyOnWriteArrayListTest extends ListTest {
List<Integer> containerInitializer() {
return new CopyOnWriteArrayList<Integer>(
new CountingIntegerList(containerSize));
}
CopyOnWriteArrayListTest(int nReaders, int nWriters) {
super("CopyOnWriteArrayList", nReaders, nWriters);
}
}
public class ListComparisons {
public static void main(String[] args) {
Tester.initMain(args);
new SynchronizedArrayListTest(10, 0);
new SynchronizedArrayListTest(9, 1);
new SynchronizedArrayListTest(5, 5);
new CopyOnWriteArrayListTest(10, 0);
new CopyOnWriteArrayListTest(9, 1);
new CopyOnWriteArrayListTest(5, 5);
Tester.exec.shutdown();
}
} /* Output: (Sample)
Type Read time Write time
Synched ArrayList 10r 0w 232158294700 0
Synched ArrayList 9r 1w 198947618203 24918613399
readTime + writeTime = 223866231602
Synched ArrayList 5r 5w 117367305062 132176613508
readTime + writeTime = 249543918570
CopyOnWriteArrayList 10r 0w 758386889 0
CopyOnWriteArrayList 9r 1w 741305671 136145237
readTime + writeTime = 877450908
CopyOnWriteArrayList 5r 5w 212763075 67967464300
readTime + writeTime = 68180227375
*///:~
```

<!--p942-->
In ListTest, the Reader and Writer classes perform the specific actions for a List<Integer>. In Reader.putResults( ), the duration is stored but so is the result, to prevent the calculations from being optimized away. startReadersAndWriters( ) is then defined to create and execute the specific Readers and Writers. Once ListTest is created, it must be further inherited to override containerInitializer( ) to create and initialize the specific test containers. In main( ), you can see variations on the tests with different numbers of readers and writers. You can change the test variables using command-line arguments because of the call to Tester.initMain(args). Concurrency The default behavior is to run each test 10 times; this helps stabilize the output, which can change because of JVM activities like hotspot optimization and garbage collection.25 The sample output that you see has been edited to show only the last iteration from each test. From the output, you can see that a synchronized ArrayList has roughly the same performance regardless of the number of readers and writers—readers contend with other readers for locks in the same way that writers do. The CopyOnWriteArrayList, however, is dramatically faster when there are no writers, and is still significantly faster when there are five writers. It would appear that you can be fairly liberal with the use of CopyOnWriteArrayList; the impact of writing to the list does not appear to overtake the impact of synchronizing the entire list for a while. Of course, you must try the two different approaches in your specific application to know for sure which one is best. Again, note that this isn’t close to being a good benchmark for absolute numbers, and your numbers will almost certainly be different. The goal is just to give you an idea of the relative behaviors of the two types of container. Since CopyOnWriteArraySet uses CopyOnWriteArrayList, its behavior will be similar and it doesn’t need a separate test here.
## Comparing Map implementations
We can use the same framework to get a rough idea of the performance of a synchronized HashMap compared to a ConcurrentHashMap:
```java
//: concurrency/MapComparisons.java
// {Args: 1 10 10} (Fast verification check during build)
// Rough comparison of thread-safe Map performance.
import java.util.concurrent.*;
import java.util.*;
import net.mindview.util.*;
abstract class MapTest
extends Tester<Map<Integer,Integer>> {
MapTest(String testId, int nReaders, int nWriters) {
super(testId, nReaders, nWriters);
}
class Reader extends TestTask {
long result = 0;
void test() {
for(long i = 0; i < testCycles; i++)
for(int index = 0; index < containerSize; index++)
result += testContainer.get(index);
}
void putResults() {
readResult += result;
readTime += duration;
}
}
class Writer extends TestTask {
void test() {
for(long i = 0; i < testCycles; i++)
for(int index = 0; index < containerSize; index++)
testContainer.put(index, writeData[index]);
}
void putResults() {
writeTime += duration;
}
```

<!--p943-->
25 For an introduction to benchmarking under the influence of Java’s dynamic compilation, see www- 128.ibm.com/developerworks/library/j-jtp12214.
```java
}
void startReadersAndWriters() {
for(int i = 0; i < nReaders; i++)
exec.execute(new Reader());
for(int i = 0; i < nWriters; i++)
exec.execute(new Writer());
}
}
class SynchronizedHashMapTest extends MapTest {
Map<Integer,Integer> containerInitializer() {
return Collections.synchronizedMap(
new HashMap<Integer,Integer>(
MapData.map(
new CountingGenerator.Integer(),
new CountingGenerator.Integer(),
containerSize)));
}
SynchronizedHashMapTest(int nReaders, int nWriters) {
super("Synched HashMap", nReaders, nWriters);
}
}
class ConcurrentHashMapTest extends MapTest {
Map<Integer,Integer> containerInitializer() {
return new ConcurrentHashMap<Integer,Integer>(
MapData.map(
new CountingGenerator.Integer(),
new CountingGenerator.Integer(), containerSize));
}
ConcurrentHashMapTest(int nReaders, int nWriters) {
super("ConcurrentHashMap", nReaders, nWriters);
}
}
public class MapComparisons {
public static void main(String[] args) {
Tester.initMain(args);
new SynchronizedHashMapTest(10, 0);
new SynchronizedHashMapTest(9, 1);
new SynchronizedHashMapTest(5, 5);
new ConcurrentHashMapTest(10, 0);
new ConcurrentHashMapTest(9, 1);
new ConcurrentHashMapTest(5, 5);
Tester.exec.shutdown();
}
} /* Output: (Sample)
Type Read time Write time
Synched HashMap 10r 0w 306052025049 0
Synched HashMap 9r 1w 428319156207 47697347568
readTime + writeTime = 476016503775
Synched HashMap 5r 5w 243956877760 244012003202
readTime + writeTime = 487968880962
ConcurrentHashMap 10r 0w 23352654318 0
ConcurrentHashMap 9r 1w 18833089400 1541853224
readTime + writeTime = 20374942624
ConcurrentHashMap 5r 5w 12037625732 11850489099
readTime + writeTime = 23888114831
*///:~
```

<!--p944-->
The impact of adding writers to a ConcurrentHashMap is even less evident than for a CopyOnWriteArrayList, but the ConcurrentHashMap uses a different technique that clearly minimizes the impact of writes. Concurrency Optimistic locking Although Atomic objects perform atomic operations like decrementAndGet( ), some Atomic classes also allow you to perform what is called "optimistic locking." This means that you do not actually use a mutex when you are performing a calculation, but after the calculation is finished and you’re ready to update the Atomic object, you use a method called compareAndSet( ). You hand it the old value and the new value, and if the old value doesn’t agree with the value it finds in the Atomic object, the operation fails—this means that some other task has modified the object in the meantime. Remember that we would ordinarily use a mutex (synchronized or Lock)to prevent more than one task modifying an object at the same time, but here we are "optimistic" by leaving the data unlocked and hoping that no other task comes along and modifies it. Again, all this is done in the name of performance—by using an Atomic instead of synchronized or Lock, you might gain performance benefits. What happens if the compareAndSet( ) operation fails? This is where it gets tricky, and where you are limited in applying this technique only to problems that can be molded to the requirements. If compareAndSet( ) fails, you must decide what to do; this is very important because if you can’t do something to recover, then you cannot use this technique and must use conventional mutexes instead. Perhaps you can retry the operation and it will be OK if you get it the second time. Or perhaps it’s OK just to ignore the failure—in some simulations, if a data point is lost, it will eventually be made up in the grand scheme of things (of course, you must understand your model well enough to know whether this is true). Consider a fictitious simulation that consists of 100,000 "genes" of length 30; perhaps this is the beginning of some kind of genetic algorithm. Suppose that for each "evolution" of the genetic algorithm, some very expensive calculations take place, so you decide to use a multiprocessor machine to distribute the tasks and improve performance. In addition, you use Atomic objects instead of Lock objects to prevent mutex overhead. (Naturally, you only produced this solution after first writing the code in the simplest way that could possibly work, using the synchronized keyword. Once you had the program running, only then did you discover that it was too slow, and begin applying performance techniques!) Because of the nature of your model, if there’s a collision during a calculation, the task that discovers the collision can just ignore it and not update its value. Here’s what it looks like:

<!--p945-->
```java
//: concurrency/FastSimulation.java
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import java.util.*;
import static net.mindview.util.Print.*;
public class FastSimulation {
static final int N_ELEMENTS = 100000;
static final int N_GENES = 30;
static final int N_EVOLVERS = 50;
static final AtomicInteger[][] GRID =
new AtomicInteger[N_ELEMENTS][N_GENES];
static Random rand = new Random(47);
static class Evolver implements Runnable {
public void run() {
while(!Thread.interrupted()) {
// Randomly select an element to work on:
int element = rand.nextInt(N_ELEMENTS);
for(int i = 0; i < N_GENES; i++) {
int previous = element - 1;
if(previous < 0) previous = N_ELEMENTS - 1;
int next = element + 1;
if(next >= N_ELEMENTS) next = 0;
int oldvalue = GRID[element][i].get();
// Perform some kind of modeling calculation:
int newvalue = oldvalue +
GRID[previous][i].get() + GRID[next][i].get();
newvalue /= 3; // Average the three values
if(!GRID[element][i]
.compareAndSet(oldvalue, newvalue)) {
// Policy here to deal with failure. Here, we
// just report it and ignore it; our model
// will eventually deal with it.
print("Old value changed from " + oldvalue);
}
}
}
}
}
public static void main(String[] args) throws Exception {
ExecutorService exec = Executors.newCachedThreadPool();
for(int i = 0; i < N_ELEMENTS; i++)
for(int j = 0; j < N_GENES; j++)
GRID[i][j] = new AtomicInteger(rand.nextInt(1000));
for(int i = 0; i < N_EVOLVERS; i++)
exec.execute(new Evolver());
TimeUnit.SECONDS.sleep(5);
exec.shutdownNow();
}
} /* (Execute to see output) *///:~
```
The elements are all placed inside an array with the assumption that this will help performance (this assumption will be tested in an exercise). Each Evolver object averages its value with the one before and after it, and if there’s a failure when it goes to update, it simply prints the value and goes on. Note that no mutexes appear in the program. Exercise 39:(6) Does FastSimulation.java make reasonable assumptions? Try changing the array to ordinary ints instead of AtomicInteger and using Lock mutexes. Compare the performance between the two versions of the program.
## ReadWriteLocks
ReadWriteLocks optimize the situation where you write to a data structure relatively infrequently, but multiple tasks read from it often. The ReadWriteLock allows you to have many readers at one time as long as no one is attempting to write. If the write lock is held, then no readers are allowed until the write lock is released. It’s completely uncertain whether a ReadWriteLock will improve the performance of your program, and it depends on issues like how often data is being read compared to how often it is being modified, the time of the read and write operations (the lock is more complex, so short operations will not see the benefits), how much thread contention there is, and whether you are running on a multiprocessor machine. Ultimately, the only way to know whether a ReadWriteLock will benefit your program is to try it out. Here’s an example showing only the most basic use of ReadWriteLocks:
```java
//: concurrency/ReaderWriterList.java
import java.util.concurrent.*;
import java.util.concurrent.locks.*;
import java.util.*;
import static net.mindview.util.Print.*;
public class ReaderWriterList<T> {
```

<!--p946-->
Concurrency

<!--p947-->
```java
private ArrayList<T> lockedList;
// Make the ordering fair:
private ReentrantReadWriteLock lock =
new ReentrantReadWriteLock(true);
public ReaderWriterList(int size, T initialValue) {
lockedList = new ArrayList<T>(
Collections.nCopies(size, initialValue));
}
public T set(int index, T element) {
Lock wlock = lock.writeLock();
wlock.lock();
try {
return lockedList.set(index, element);
} finally {
wlock.unlock();
}
}
public T get(int index) {
Lock rlock = lock.readLock();
rlock.lock();
try {
// Show that multiple readers
// may acquire the read lock:
if(lock.getReadLockCount() > 1)
print(lock.getReadLockCount());
return lockedList.get(index);
} finally {
rlock.unlock();
}
}
public static void main(String[] args) throws Exception {
new ReaderWriterListTest(30, 1);
}
}
class ReaderWriterListTest {
ExecutorService exec = Executors.newCachedThreadPool();
private final static int SIZE = 100;
private static Random rand = new Random(47);
private ReaderWriterList<Integer> list =
new ReaderWriterList<Integer>(SIZE, 0);
private class Writer implements Runnable {
public void run() {
try {
for(int i = 0; i < 20; i++) { // 2 second test
list.set(i, rand.nextInt());
TimeUnit.MILLISECONDS.sleep(100);
}
} catch(InterruptedException e) {
// Acceptable way to exit
}
print("Writer finished, shutting down");
exec.shutdownNow();
}
}
private class Reader implements Runnable {
public void run() {
try {
while(!Thread.interrupted()) {
for(int i = 0; i < SIZE; i++) {
list.get(i);
TimeUnit.MILLISECONDS.sleep(1);
}
```
Concurrency
```java
}
} catch(InterruptedException e) {
// Acceptable way to exit
}
}
}
public ReaderWriterListTest(int readers, int writers) {
for(int i = 0; i < readers; i++)
exec.execute(new Reader());
for(int i = 0; i < writers; i++)
exec.execute(new Writer());
}
} /* (Execute to see output) *///:~
```

<!--p948-->
A ReaderWriterList can hold a fixed number of any type. You must give the constructor the desired size of the list and an initial object to populate the list with. The set( ) method acquires the write lock in order to call the underlying ArrayList. set( ), and the get( ) method acquires the read lock in order to call ArrayList.get( ). In addition, get( ) checks to see if more than one reader has acquired the read lock and, if so, displays that number to demonstrate that multiple readers may acquire the read lock. To test the ReaderWriterList, ReaderWriterListTest creates both reader and writer tasks for a ReaderWriterList<Integer>. Notice that there are far fewer writes than reads. If you look at the JDK documentation for ReentrantReadWriteLock, you’ll see that there are a number of other methods available, as well as issues of "fairness" and "policy decisions." This is a rather sophisticated tool, and one to use only when you are casting about for ways to improve performance. Your first draft of your program should use straightforward synchronization, and only if necessary should you introduce ReadWriteLock. Exercise 40: (6) Following the example of ReaderWriterList.java, create a ReaderWriterMap using a HashMap. Investigate its performance by modifying MapComparisons.java. How does it compare to a synchronized HashMap and a ConcurrentHashMap? Active objects After working your way through this chapter, you may observe that threading in Java seems very complex and difficult to use correctly. In addition, it can seem a bit counterproductive— although tasks work in parallel, you must invest great effort to implement techniques that prevent those tasks from interfering with each other. If you’ve ever written assembly language, writing threaded programs has a similar feel: Every detail matters, you’re responsible for everything, and there’s no safety net in the form of compiler checking. Could there be a problem with the threading model itself? After all, it comes relatively unchanged from the world of procedural programming. Perhaps there is a different model for concurrency that is a better fit for objectoriented programming. One alternative approach is called active objects or actors.26The reason the objects are called "active" is that each object maintains its own worker thread and message queue, and all requests to that object are enqueued, to be run one at a time. So with active objects, we 26 Thanks to Allen Holub for taking the time to explain this to me. serialize messages rather than methods, which means we no longer need to guard against problems that happen when a task is interrupted midway through its loop. When you send a message to an active object, that message is transformed into a task that goes on the object’s queue to be run at some later point. The Java SE5 Future comes in handy for implementing this scheme. Here’s a simple example that has two methods which enqueue method calls:

<!--p949-->
```java
//: concurrency/ActiveObjectDemo.java
// Can only pass constants, immutables, "disconnected
// objects," or other active objects as arguments
// to asynch methods.
import java.util.concurrent.*;
import java.util.*;
import static net.mindview.util.Print.*;
public class ActiveObjectDemo {
private ExecutorService ex =
Executors.newSingleThreadExecutor();
private Random rand = new Random(47);
// Insert a random delay to produce the effect
// of a calculation time:
private void pause(int factor) {
try {
TimeUnit.MILLISECONDS.sleep(
100 + rand.nextInt(factor));
} catch(InterruptedException e) {
print("sleep() interrupted");
}
}
public Future<Integer>
calculateInt(final int x, final int y) {
return ex.submit(new Callable<Integer>() {
public Integer call() {
print("starting " + x + " + " + y);
pause(500);
return x + y;
}
});
}
public Future<Float>
calculateFloat(final float x, final float y) {
return ex.submit(new Callable<Float>() {
public Float call() {
print("starting " + x + " + " + y);
pause(2000);
return x + y;
}
});
}
public void shutdown() { ex.shutdown(); }
public static void main(String[] args) {
ActiveObjectDemo d1 = new ActiveObjectDemo();
// Prevents ConcurrentModificationException:
List<Future<?>> results =
new CopyOnWriteArrayList<Future<?>>();
for(float f = 0.0f; f < 1.0f; f += 0.2f)
results.add(d1.calculateFloat(f, f));
for(int i = 0; i < 5; i++)
results.add(d1.calculateInt(i, i));
print("All asynch calls made");
while(results.size() > 0) {
for(Future<?> f : results)
if(f.isDone()) {
try {
print(f.get());
} catch(Exception e) {
throw new RuntimeException(e);
}
results.remove(f);
}
}
d1.shutdown();
}
} /* Output: (85% match)
All asynch calls made
starting 0.0 + 0.0
starting 0.2 + 0.2
0.0
starting 0.4 + 0.4
0.4
starting 0.6 + 0.6
0.8
starting 0.8 + 0.8
1.2
starting 0 + 0
1.6
starting 1 + 1
starting 2 + 2
starting 3 + 3
starting 4 + 4
*///:~
```

<!--p950-->

<!--p951-->

<!--p952-->

<!--p953-->
The "single thread executor" produced by the call to Executors.newSingleThreadExecutor( ) maintains its own unbounded blocking queue, and has only one thread taking tasks off the queue and running them to completion. All we need to do in calculateInt( ) and calculateFloat( ) is to submit( ) a new Callable object in response to a method call, thus converting method calls into messages. The method body is contained within the call( ) method in the anonymous inner class. Notice that the return value of each active object method is a Future with a generic parameter that is the actual return type of the method. This way, the method call returns almost immediately, and the caller uses the Future to discover when the task completes and to collect the actual return value. This handles the most complex case, but if the call has no return value, then the process is simplified. In main( ), a List<Future<?>> is created to capture the Future objects returned by the calculateFloat( ) and calculateInt( ) messages sent to the active object. This list is polled using isDone( ) for each Future, which is removed from the List when it completes and its results are processed. Notice that the use of CopyOnWriteArrayList removes the need to copy the List in order to prevent ConcurrentModificationExceptions. In order to inadvertently prevent coupling between threads, any arguments to pass to an active-object method call must be either read-only, other active objects, or disconnected objects (my term), which are objects that have no connection to any other task (this is hard to enforce because there’s no language support for it). With active objects: Concurrency 1. Each object has its own worker thread. 2. Each object maintains total control of its own fields (which is somewhat more rigorous than normal classes, which only have the option of guarding their fields). 3. All communication between active objects happens in the form of messages between those objects. 4. All messages between active objects are enqueued. The results are quite compelling. Since a message from one active object to another can only be blocked by the delay in enqueuing it, and because that delay is always very short and is not dependent on any other objects, the sending of a message is effectively unblockable (the worst that will happen is a short delay). Since an active-object system only communicates via messages, two objects cannot be blocked while contending to call a method on another object, and this means that deadlock cannot occur, which is a big step forward. Because the worker thread within an active object only executes one message at a time, there is no resource contention and you don’t have to worry about synchronizing methods. Synchronization still happens, but it happens on the message level, by enqueuing the method calls so that only one can happen at a time. Unfortunately, without direct compiler support, the coding approach shown above is too cumbersome. However, progress is occurring in the field of active objects and actors, and more interestingly, in the field called agent-based programming. Agents are effectively active objects, but agent systems also support transparency across networks and machines. It would not surprise me if agent-based programming becomes the eventual successor to objectoriented programming, because it combines objects with a relatively easy concurrency solution. You can find more information about active objects, actors and agents by searching the Web. In particular, some of the ideas behind active objects come from C.A.R. Hoare’s theory of Communicating Sequential Processes (CSP). Exercise 41:(6) Add a message handler to ActiveObjectDemo.java that has no return value, and call this within main( ). Exercise 42:(7) Modify WaxOMatic.java so that it implements active objects. Project:27Use annotations and Javassist to create a class annotation @Active that transforms the target class into an active object. 27 Projects are suggestions to be used (for example) as term projects. Solutions to projects are not included in the solution guide. Summary The goal of this chapter was to give you the foundations of concurrent programming with Java threads, so that you understand that: 1.You can run multiple independent tasks. 2.You must consider all the possible problems when these tasks shut down. 3.Tasks can interfere with each other over shared resources. The mutex (lock) is the basic tool used to prevent these collisions. 4.Tasks can deadlock if they are not carefully designed. It is vital to learn when to use concurrency and when to avoid it. The main reasons to use it are: • To manage a number of tasks whose intermingling will use the computer more efficiently (including the ability to transparently distribute the tasks across multiple CPUs). • To allow better code organization. • To be more convenient for the user. The classic example of resource balancing is to use the CPU during I/O waits. Better code organization is typically seen in simulations. The classic example of user convenience is to monitor a "stop" button during long downloads. An additional advantage to threads is that they provide "light" execution context switches (on the order of 100 instructions) rather than "heavy" process context switches (thousands of instructions). Since all threads in a given process share the same memory space, a light context switch changes only program execution and local variables. A process change—the heavy context switch—must exchange the full memory space. The main drawbacks to multithreading are: 1.Slowdown occurs while threads are waiting for shared resources. 2.Additional CPU overhead is required to manage threads. 3.Unrewarded complexity arises from poor design decisions. 4.Opportunities are created for pathologies such as starving, racing, deadlock, and livelock (multiple threads working individual tasks that the ensemble can’t finish). 5.Inconsistencies occur across platforms. For instance, while developing some of the examples for this book, I discovered race conditions that quickly appeared on some computers but that wouldn’t appear on others. If you develop a program on the latter, you might get badly surprised when you distribute it. One of the biggest difficulties with threads occurs because more than one task might be sharing a resource—such as the memory in an object—and you must make sure that multiple tasks don’t try to read and change that resource at the same time. This requires judicious use of the available locking mechanisms (for example, the synchronized keyword). These are essential tools, but they must be understood thoroughly because they can quietly introduce deadlock situations. Concurrency In addition, there’s an art to the application of threads. Java is designed to allow you to create as many objects as you need to solve your problem—at least in theory. (Creating millions of objects for an engineering finite-element analysis, for example, might not be practical in Java without the use of the Flyweight design pattern.) However, it seems that there is an upper bound to the number of threads you’ll want to create, because at some number, threads seem to become balky. This critical point can be hard to detect and will often depend on the OS and JVM; it can be less than a hundred or in the thousands. As you will often create only a handful of threads to solve a problem, this is typically not much of a limit, but in a more general design it becomes a constraint that might force you to add a cooperative concurrency scheme. Regardless of how simple threading can seem using a particular language or library, consider it a black art. There’s always something that can bite you when you least expect it. The reason that the dining philosophers problem is interesting is that it can be adjusted so that deadlock rarely happens, giving you the impression that everything is copacetic. In general, use threading carefully and sparingly. If your threading issues get large and complex, consider using a language like Erlang. This is one of several functional languages that are specialized for threading. It may be possible to use such a language for the portions of your program that demand threading, if you are doing lots of it, and if it’s complicated enough to justify this approach. Concurrency Further reading Unfortunately, there is a lot of misleading information about concurrency— this emphasizes how confusing it can be, and how easy it is to think that you understand the issues (I know, because I’ve been under the impression that I’ve understood threading numerous times in the past, and I have no doubt that there will be more epiphanies for me in the future). There’s always a bit of sleuthing required when you pick up a new document about concurrency, to try to understand how much the writer does and doesn’t understand. Here are some books that I think I can safely say are reliable: Java Concurrency in Practice, by Brian Goetz, Tim Peierls, Joshua Bloch, Joseph Bowbeer, David Holmes, and Doug Lea (Addison-Wesley, 2006). Basically, the "who’s who" in the Java threading world. Concurrent Programming in Java, Second Edition, by Doug Lea (Addison-Wesley, 2000). Although this book significantly predates Java SE5, much of Doug’s work became the new java.util.concurrent libraries, so this book is essential for a complete understanding of concurrency issues. It goes beyond Java concurrency and discusses current thinking across languages and technologies. Although it can be obtuse in places, it merits rereading several times (preferably with months in between in order to internalize the information). Doug is one of the few people in the world who actually understand concurrency, so this is a worthwhile endeavor. The Java Language Specification, Third Edition (Chapter 17), by Gosling, Joy, Steele, and Bracha (Addison-Wesley, 2005). The technical specification, conveniently available as an electronic document: http://java.sun.com/docs/books/jls. Solutions to selected exercises can be found in the electronic document The Thinking in Java Annotated Solution Guide, available for sale from www.MindView.net.