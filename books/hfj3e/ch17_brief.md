# Chapter 17: Chapter 17: Make a Connection

pages 625-676

another machine. It’s easy. All the low-level networking details are taken care of by the built- in Java libraries. One of Java’s big benefits is that sending and receiving data over a network can be just I/O with a slightly different connection at the end of the I/O chain. In this chapter we’ll connect to the outside world with channels. We’ll make client channels. We’ll make server channels. We’ll make clients and servers, and we’ll make them talk to each other. And we’ll also

have to learn how to do more than one thing at once. Before the chapter’s done, you’ll have a fully functional, multithreaded chat client. Did we just say multithreaded? Yes, now you will learn the secret of how to talk to Bob while simultaneously listening to Suzy. this is a new chapter beatbox chat skyler4: fast and funky, good for sequence 12 evster2: like skyler2, but more Oakenfoldish skyler5: you WISH! Too perky

## Real-time BeatBox chat

## Chat program overview

## Connecting, sending, and receiving

There’s a lot of low-level stuff that has to happen for these things to work. But we’re lucky, because the Java APIs make it a piece of cake for programmers. You’ll see a lot more GUI code than networking and I/O code in this chapter. And that’s not all. Lurking within the simple chat client is a problem we haven’t faced so far in this book: doing two things at the same time. Establishing a connection is a one-time operation (that either works or fails). But after that, a chat participant wants to send outgoing messages and simultaneously receive incoming messages from the other participants (via the server). Hmm...that one’s going to take a little thought, but we’ll get there in just a few pages.

## 1. Connect

```java
InetSocketAddress serverAddress = new InetSocketAddress("196.164.1.103", 5000);
SocketChannel socketChannel = SocketChannel.open(serverAddress);
```

## 2. Receive

```java
SocketAddress serverAddr = new InetSocketAddress("127.0.0.1", 5000);
SocketChannel socketChannel = SocketChannel.open(serverAddr);
```

```java
BufferedReader bufferedReader = new BufferedReader(reader);
String message = bufferedReader.readLine();
```

```java
Reader reader = Channels.newReader(socketChannel, StandardCharsets.UTF_8);
```

## 3. Send

```java
SocketAddress serverAddr = new InetSocketAddress("127.0.0.1", 5000);
SocketChannel socketChannel = SocketChannel.open(serverAddr);
```

```java
PrintWriter printWriter = new PrintWriter(writer);
writer.println("message to send");
writer.print("another message");
```

```java
Writer writer = Channels.newWriter(socketChannel, StandardCharsets.UTF_8);
```

```java
Socket chatSocket = new Socket("127.0.0.1", 5000);
InputStreamReader in = new InputStreamReader(chatSocket.getInputStream());
BufferedReader reader = new BufferedReader(in);
String message = reader.readLine();
PrintWriter writer = new PrintWriter(chatSocket.getOutputStream());
writer.println("message to send");
writer.print("another message");
```

## The DailyAdviceClient

```java
import java.io.*;
import java.net.InetSocketAddress;
import java.nio.channels.Channels;
import java.nio.channels.SocketChannel;
import java.nio.charset.StandardCharsets;
public class DailyAdviceClient {
public void go() {
InetSocketAddress serverAddress = new InetSocketAddress("127.0.0.1", 5000);
try (SocketChannel socketChannel = SocketChannel.open(serverAddress)) {
Reader channelReader = Channels.newReader(socketChannel, StandardCharsets.UTF_8);
BufferedReader reader = new BufferedReader(channelReader);
String advice = reader.readLine();
System.out.println("Today you should: " + advice);
reader.close();
} catch (IOException e) {
e.printStackTrace();
}
}
public static void main(String[] args) {
new DailyAdviceClient().go();
}
}
```

## DailyAdviceClient code

## Writing a simple server application

```java
ServerSocketChannel serverChannel = ServerSocketChannel.open();
serverChannel.bind(new InetSocketAddress(5000));
```

```java
SocketChannel svr = SocketChannel.open(new InetSocketAddress("190.165.1.103", 5000));
```

```java
SocketChannel clientChannel = serverChannel.accept();
```

```java
import java.io.*;
import java.net.InetSocketAddress;
import java.nio.channels.*;
import java.util.Random;
public class DailyAdviceServer {
final private String[] adviceList = {
"Take smaller bites",
"Go for the tight jeans. No they do NOT make you look fat.",
"One word: inappropriate",
"Just for today, be honest. Tell your boss what you *really* think",
"You might want to rethink that haircut."};
private final Random random = new Random();
public void go() {
try (ServerSocketChannel serverChannel = ServerSocketChannel.open()) {
serverChannel.bind(new InetSocketAddress(5000));
while (serverChannel.isOpen()) {
SocketChannel clientChannel = serverChannel.accept();
PrintWriter writer = new PrintWriter(Channels.newOutputStream(clientChannel));
String advice = getAdvice();
writer.println(advice);
writer.close();
System.out.println(advice);
}
} catch (IOException ex) {
ex.printStackTrace();
}
}
private String getAdvice() {
int nextAdvice = random.nextInt(adviceList.length);
return adviceList[nextAdvice];
}
public static void main(String[] args) {
new DailyAdviceServer().go();
}
}
```

## DailyAdviceServer code

This program makes a ServerSocketChannel and waits for client requests. When it gets a client request (i.e., client created a new SocketChannel to this server), the server makes a new SocketChannel to that client. The server makes a PrintWriter (using a Writer created from the SocketChannel) and sends a message to the client. Remember the imports. Daily advice comes from this array. ServerSocketChannel makes this server

```java
Writer writer = Channels.newWriter(sockCh,
StandardCharsets.UTF_8);
```

## Writing a Chat Client

```java
public class SimpleChatClientA {
private JTextField outgoing;
private PrintWriter writer;
public void go() {
// call the setUpNetworking() method
// make gui and register a listener with the send button
}
private void setUpNetworking() {
// open a SocketChannel to the server
// make a PrintWriter and assign to writer instance variable
}
private void sendMessage() {
// get the text from the text field and
// send it to the server using the writer (a PrintWriter)
}
}
```

```java
import javax.swing.*;
import java.awt.*;
import java.io.*;
import java.net.InetSocketAddress;
import java.nio.channels.*;
import static java.nio.charset.StandardCharsets.UTF_8;
public class SimpleChatClientA {
private JTextField outgoing;
private PrintWriter writer;
public void go() {
setUpNetworking();
outgoing = new JTextField(20);
JButton sendButton = new JButton("Send");
sendButton.addActionListener(e -> sendMessage());
JPanel mainPanel = new JPanel();
mainPanel.add(outgoing);
mainPanel.add(sendButton);
JFrame frame = new JFrame("Ludicrously Simple Chat Client");
frame.getContentPane().add(BorderLayout.CENTER, mainPanel);
frame.setSize(400, 100);
frame.setVisible(true);
frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
}
private void setUpNetworking() {
try {
InetSocketAddress serverAddress = new InetSocketAddress("127.0.0.1", 5000);
SocketChannel socketChannel = SocketChannel.open(serverAddress);
writer = new PrintWriter(Channels.newWriter(socketChannel, UTF_8));
System.out.println("Networking established.");
} catch (IOException e) {
e.printStackTrace();
}
}
private void sendMessage() {
writer.println(outgoing.getText());
writer.flush();
outgoing.setText("");
outgoing.requestFocus();
}
public static void main(String[] args) {
new SimpleChatClientA().go();
}
}
```

You can use this server code for all versions of the Chat Client. Every possible disclaimer ever disclaimed is in effect here. To keep the code stripped down to the bare essentials, we took out a lot of parts that you’d need to make this a real server. In other words, it works, but there are at least a hundred ways to break it. If you want to really sharpen your skills after you’ve finished this book, come back and make this server code more robust.

```java
import java.io.*;
import java.net.InetSocketAddress;
import java.nio.channels.*;
import java.util.*;
import java.util.concurrent.*;
import static java.nio.charset.StandardCharsets.UTF_8;
public class SimpleChatServer {
private final List<PrintWriter> clientWriters = new ArrayList<>();
public static void main(String[] args) {
new SimpleChatServer().go();
}
public void go() {
ExecutorService threadPool = Executors.newCachedThreadPool();
try {
ServerSocketChannel serverSocketChannel = ServerSocketChannel.open();
serverSocketChannel.bind(new InetSocketAddress(5000));
while (serverSocketChannel.isOpen()) {
SocketChannel clientSocket = serverSocketChannel.accept();
PrintWriter writer = new PrintWriter(Channels.newWriter(clientSocket, UTF_8));
clientWriters.add(writer);
threadPool.submit(new ClientHandler(clientSocket));
System.out.println("got a connection");
}
} catch (IOException ex) {
ex.printStackTrace();
}
}
```

understand it much better if you work out what’s happening than if we explained it to you. Then again, this is Ready-Bake Code, so you really don’t have to understand it at all. It’s here just to support the two versions of the Chat Client. Ready-Bake Code To run the Chat Client, you need two terminals. First, launch this server from one terminal, and then launch the client from another terminal. chat server code

```java
private void tellEveryone(String message) {
for (PrintWriter writer : clientWriters) {
writer.println(message);
writer.flush();
}
}
public class ClientHandler implements Runnable {
BufferedReader reader;
SocketChannel socket;
public ClientHandler(SocketChannel clientSocket) {
socket = clientSocket;
reader = new BufferedReader(Channels.newReader(socket, UTF_8));
}
public void run() {
String message;
try {
while ((message = reader.readLine()) != null) {
System.out.println("read " + message);
tellEveryone(message);
}
} catch (IOException ex) {
ex.printStackTrace();
}
}
}
}
```

```java
got a connection
read Nice to meet you
```

```java
Networking established. Client
running at: /127.0.0.1:57531
```

Cons: How does the server know what you’ve seen and what you haven’t? The server would have to store the messages, rather than just doing a distribute-and-forget each time it gets one. And why 20 seconds? A delay like this affects usability, but as you reduce the delay, you risk hitting your server needlessly. Inefficient. Option Two: Poll the server every 20 seconds. Option Three: Read messages as soon as they’re sent from the server.

Cons: How do you do two things at the same time? Where would you put this code? You’d need a loop somewhere that was always waiting to read from the server. But where would that go? Once you launch the GUI, nothing happens until an event is fired by a GUI component. improving the chat client Option One: Read something in from the server each time the user sends a message. Pros: Doable, very easy. Cons: Stupid. Why choose such an arbitrary time to check for messages? What if a user is a

you’re running on a multiprocessor system (like most modern computers and phones), you can actually do more than one thing at a time. With Java threads, even if you’re not running on a multiprocessor system or if you’re running more processes than available cores, it can appear that you’re doing all these things simultaneously. In other words, execution can move back and forth between stacks so rapidly that you feel as though all stacks are executing at the same time. Remember, Java is just a process running on your underlying OS. So first, Java itself has to be “the currently executing process” on the OS. But once Java gets its turn to execute, exactly what does the JVM run? Which bytecodes execute? Whatever is on the top of the currently running stack! And in 100 milliseconds, the currently executing code might switch to a different method on a different stack.

```java
public static void main(String[] args) {
...
}
```

```java
Runnable r = new MyThreadJob();
Thread t = new Thread(r);
t.start();
Dog d = new Dog();
```

```java
public void run() {
// code that will be run by the new thread
}
```

## To create a new call stack you need a job to run

```java
public class MyRunnable implements Runnable {
public void run() {
go();
}
public void go() {
doMore();
}
public void doMore() {
System.out.println(Thread.currentThread().getName() +
": top o’ the stack");
Thread.dumpStack();
}
}
```

```java
class RunTester {
public static void main(String[] args) {
MyRunnable runnable = new MyRunnable();
runnable.run();
System.out.println(Thread.currentThread().getName() +
": back in main");
Thread.dumpStack();
}
}
```

```java
class ThreadTester {
public static void main(String[] args) {
Runnable threadJob = new MyRunnable();
Thread myThread = new Thread(threadJob);
myThread.start();
System.out.println(
Thread.currentThread().getName() +
": back in main");
Thread.dumpStack();
}
}
```

## How we used to launch a new thread

```java
main: back in main
Thread-0: top o’ the stack
java.lang.Exception: Stack trace
at java.base/java.lang.Thread.dumpStack(Thread.java:1383)
at ThreadTester.main(MyRunnable.java:38)
java.lang.Exception: Stack trace
at java.base/java.lang.Thread.dumpStack(Thread.java:1383)
at MyRunnable.doMore(MyRunnable.java:15)
at MyRunnable.go(MyRunnable.java:10)
at MyRunnable.run(MyRunnable.java:6)
at java.base/java.lang.Thread.run(Thread.java:829)
```

downside is you have to control it. You have to keep track of all the Threads and make sure they’re shut down at the end. Wouldn’t it be better to have something else that starts, stops, and even reuses the Threads so you don’t have to? Allow us to introduce an interface in java.util.concurrent, ExecutorService. Implementations of this interface will execute jobs (Runnables). Behind the scenes the ExecutorService will create, reuse, and kill threads in order to run these jobs.

```java
class ExecutorTester {
public static void main(String[] args) {
Runnable job = new MyRunnable();
ExecutorService executor = Executors.newSingleThreadExecutor();
executor.execute(job);
System.out.println(Thread.currentThread().getName() +
": back in main");
Thread.dumpStack();
executor.shutdown();
}
}
```

## The three states of a new thread

## The thread scheduler

## The thread scheduler

```java
class ExecutorTestDrive {
public static void main (String[] args) {
ExecutorService executor =
Executors.newSingleThreadExecutor();
executor.execute(() ->
System.out.println("top o’ the stack"));
System.out.println("back in main");
executor.shutdown();
}
}
class ThreadTestDrive {
public static void main (String[] args) {
Thread myThread = new Thread(() ->
System.out.println("top o’ the stack"));
myThread.start();
System.out.println("back in main");
}
}
```

```java
% java ExecutorTestDrive
back in main
top o’ the stack
% java ExecutorTestDrive
top o’ the stack
back in main
% java ExecutorTestDrive
top o’ the stack
back in main
% java ExecutorTestDrive
back in main
top o’ the stack
% java ExecutorTestDrive
top o’ the stack
back in main
% java ExecutorTestDrive
top o’ the stack
back in main
% java ExecutorTestDrive
back in main
top o’ the stack
```

## How did we end up with different results?

```java
executor.execute(() -> printMsg());
```

## Putting a thread to sleep

```java
Thread.sleep(2000);
```

```java
try {
Thread.sleep(2000);
} catch(InterruptedException ex) {
ex.printStackTrace();
}
```

```java
TimeUnit.MINUTES.sleep(2);
```

```java
Thread.sleep(120000);
```

```java
class PredictableSleep {
public static void main (String[] args) {
ExecutorService executor =
Executors.newSingleThreadExecutor();
executor.execute(() -> sleepThenPrint());
System.out.println("back in main");
executor.shutdown();
}
private static void sleepThenPrint() {
try {
TimeUnit.SECONDS.sleep(2);
} catch (InterruptedException e) {
e.printStackTrace();
}
System.out.println("top o’ the stack");
}
}
```

```java
% java PredictableSleep
back in main
top o’ the stack
% java PredictableSleep
back in main
top o’ the stack
% java PredictableSleep
back in main
top o’ the stack
% java PredictableSleep
back in main
top o’ the stack
% java PredictableSleep
back in main
top o’ the stack
```

If we put the thread to sleep for two seconds, the thread will be non-runnable for that time. When it wakes up, it won’t automatically become the currently running thread. When a thread wakes up, the thread is once again at the mercy of the thread scheduler. Our application is go­ ing to be hanging around for at least those two seconds, probably more. This might not sound like a big deal, but imagine a bigger program full of these pauses intentionally slowing down the application.

We put the new thread to sleep for two seconds, assuming that the main thread would be the running thread, and complete its work in that time. But what if the main thread took longer to finish than that? What if another thread, running a longer job, was scheduled instead? One of the ways people deal with this is to set sleep times that are much longer than they’d expect a job to take, but then our first problem becomes even more of a problem.

## Counting down until ready

```java
import java.util.concurrent.*;
class PredictableLatch {
public static void main (String[] args) {
ExecutorService executor = Executors.newSingleThreadExecutor();
CountDownLatch latch = new CountDownLatch(1);
executor.execute(() -> waitForLatchThenPrint(latch));
System.out.println("back in main");
latch.countDown();
executor.shutdown();
}
private static void waitForLatchThenPrint(CountDownLatch latch) {
try {
latch.await();
} catch (InterruptedException e) {
e.printStackTrace();
}
System.out.println("top o’ the stack");
}
}
```

sleep() version just one time takes over 2 seconds (2000 milliseconds), imagine how long it took to run 100 times*.... * 200331 milliseconds. That’s over 4000x slower. Create a new CountDownLatch. This latch lets us "wait for the signal." We have one event we want to wait for (the main thread prints its message), so we set this up with a value of “1.” Tell the latch to count down when the main method has printed its message.

## Pooling Threads

```java
ExecutorService threadPool =
Executors.newCachedThreadPool();
```

```java
threadPool.execute(() -> run("Job 1"));
```

```java
threadPool.execute(() -> run("Job 324"));
```

## Running multiple threads

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
public class RunThreads {
public static void main(String[] args) {
ExecutorService threadPool = Executors.newFixedThreadPool(2);
threadPool.execute(() -> runJob("Job 1"));
threadPool.execute(() -> runJob("Job 2"));
threadPool.shutdown();
}
public static void runJob(String jobName) {
for (int i = 0; i < 25; i++) {
String threadName = Thread.currentThread().getName();
System.out.println(jobName + " is running on " + threadName);
}
}
}
```

```java
Job 1 is running on pool-1-thread-1
Job 2 is running on pool-1-thread-2
Job 2 is running on pool-1-thread-2
Job 1 is running on pool-1-thread-1
Job 2 is running on pool-1-thread-2
Job 1 is running on pool-1-thread-1
Job 2 is running on pool-1-thread-2
Job 1 is running on pool-1-thread-1
Job 2 is running on pool-1-thread-2
Job 1 is running on pool-1-thread-1
Job 1 is running on pool-1-thread-1
Job 1 is running on pool-1-thread-1
Job 1 is running on pool-1-thread-1
Job 1 is running on pool-1-thread-1
Job 1 is running on pool-1-thread-1
Job 1 is running on pool-1-thread-1
```

## Closing time at the thread pool

main methods. Although the thread pools will take care of our individual Threads, we do need to be responsible adults and close the pool when we’re finished with it. That way, the pool can empty its job queue and shut down all of its threads to free up system resources. ExecutorService has two shutdown methods. You can use either, but to be safe we’d use both: Calling shutdown() asks the ExecutorService nicely if it wouldn’t mind awfully wrapping things up

All of the Threads that are currently running jobs are allowed to finish those jobs, and any jobs waiting in the queue will also be finished off. The ExecutorService will reject any new jobs too. If you need your code to wait until all of those things are finished, you can use awaitTermination to sit and wait until it’s finished. You give awaitTermination a maximum amount of time to wait for everything to end, so awaitTermination will hang around until either the ExecutorService has finished everything or the timeout has been reached, whichever is earlier.

```java
public class ClosingTime {
public static void main(String[] args) {
ExecutorService threadPool = Executors.newFixedThreadPool(2);
threadPool.execute(new LongJob("Long Job"));
threadPool.execute(new ShortJob("Short Job"));
threadPool.shutdown();
try {
boolean finished = threadPool.awaitTermination(5, TimeUnit.SECONDS);
System.out.println("Finished? " + finished);
} catch (InterruptedException e) {
e.printStackTrace();
}
threadPool.shutdownNow();
}
}
```

Everybody out! When this is called, the ExecutorService will try to stop any Threads that are running, will not run any waiting jobs, and definitely won’t let anyone else into the pool. Use this if you need to put a stop to everything. This is sometimes used after first calling shutdown() to give the jobs a chance to finish before pulling the plug entirely. Start two jobs, a short one that just prints the name and a “long”

```java
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.net.InetSocketAddress;
import java.nio.channels.*;
import java.util.concurrent.*;
import static java.nio.charset.StandardCharsets.UTF_8;
public class SimpleChatClient {
private JTextArea incoming;
private JTextField outgoing;
private BufferedReader reader;
private PrintWriter writer;
public void go() {
setUpNetworking();
JScrollPane scroller = createScrollableTextArea();
outgoing = new JTextField(20);
JButton sendButton = new JButton("Send");
sendButton.addActionListener(e -> sendMessage());
JPanel mainPanel = new JPanel();
mainPanel.add(scroller);
mainPanel.add(outgoing);
mainPanel.add(sendButton);
ExecutorService executor = Executors.newSingleThreadExecutor();
executor.execute(new IncomingReader());
JFrame frame = new JFrame("Ludicrously Simple Chat Client");
frame.getContentPane().add(BorderLayout.CENTER, mainPanel);
frame.setSize(400, 350);
frame.setVisible(true);
frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
}
```

## New and improved SimpleChatClient

Way back near the beginning of the chapter, we built the SimpleChatClient that could send outgoing messages to the server but couldn’t receive anything. Remember? That’s how we got onto this whole thread topic in the first place, because we needed a way to do two things at once: send messages to the server (interacting with the GUI) while simultaneously reading incoming messages from the server, displaying them in the scrolling text area.

This is the New Improved chat client that can both send and receive messages, thanks to the power of multithreading! Remember, you need to run the chat server first to run this code. This is mostly GUI code you’ve seen before. Nothing special except the highlighted part where we start the new “reader” thread. We’ve got a new job, an inner class, which is a Runnable. The job is to read from the server’s socket stream, displaying any incoming messages in the scrolling text area. We start this job using a single thread executor since we know we want to run only this one job.

```java
private JScrollPane createScrollableTextArea() {
incoming = new JTextArea(15, 30);
incoming.setLineWrap(true);
incoming.setWrapStyleWord(true);
incoming.setEditable(false);
JScrollPane scroller = new JScrollPane(incoming);
scroller.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS);
scroller.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
return scroller;
}
private void setUpNetworking() {
try {
InetSocketAddress serverAddress = new InetSocketAddress("127.0.0.1", 5000);
SocketChannel socketChannel = SocketChannel.open(serverAddress);
reader = new BufferedReader(Channels.newReader(socketChannel, UTF_8));
writer = new PrintWriter(Channels.newWriter(socketChannel, UTF_8));
System.out.println("Networking established.");
} catch (IOException ex) {
ex.printStackTrace();
}
}
private void sendMessage() {
writer.println(outgoing.getText());
writer.flush();
outgoing.setText("");
outgoing.requestFocus();
}
public class IncomingReader implements Runnable {
public void run() {
String message;
try {
while ((message = reader.readLine()) != null) {
System.out.println("read " + message);
incoming.append(message + "\n");
}
} catch (IOException ex) {
ex.printStackTrace();
}
}
}
public static void main(String[] args) {
new SimpleChatClient().go();
}
}
```

```java
% java PingingClient
Networking established
09:27:06 Sent ping 0
09:27:07 Sent ping 1
09:27:08 Sent ping 2
09:27:09 Sent ping 3
09:27:10 Sent ping 4
09:27:11 Sent ping 5
09:27:12 Sent ping 6
09:27:13 Sent ping 7
09:27:14 Sent ping 8
09:27:15 Sent ping 9
```

```java
public class PingingClient {
import java.io.*;
import java.net.InetSocketAddress;
import java.nio.channels.*;
import java.time.format.FormatStyle;
import java.util.concurrent.TimeUnit;
writer.flush();
e.printStackTrace();
TimeUnit.SECONDS.sleep(1);
PrintWriter writer = new PrintWriter(Channels.newWriter(channel, UTF_8));
for (int i = 0; i < 10; i++) {
} catch (IOException | InterruptedException e) {
writer.println(message);
import static java.nio.charset.StandardCharsets.UTF_8;
import static java.time.LocalDateTime.now;
import static java.time.format.DateTimeFormatter.ofLocalizedTime;
String currentTime = now().format(ofLocalizedTime(FormatStyle.MEDIUM));
System.out.println(currentTime + " Sent " + message);
System.out.println("Networking established");
InetSocketAddress server = new InetSocketAddress("127.0.0.1", 5000);
try (SocketChannel channel = SocketChannel.open(server)) {
String message = "ping " + i;
}
}
public static void main(String [] args) {
}
}
```

```java
import java.io.*;
import java.net.InetSocketAddress;
import java.nio.channels.*;
import java.time.format.FormatStyle;
import java.util.concurrent.TimeUnit;
import static java.nio.charset.StandardCharsets.UTF_8;
import static java.time.LocalDateTime.now;
import static java.time.format.DateTimeFormatter.ofLocalizedTime;
public class PingingClient {
public static void main(String[] args) {
InetSocketAddress server = new InetSocketAddress("127.0.0.1", 5000);
try (SocketChannel channel = SocketChannel.open(server)) {
PrintWriter writer = new PrintWriter(Channels.newWriter(channel, UTF_8));
System.out.println("Networking established");
for (int i = 0; i < 10; i++) {
String message = "ping " + i;
writer.println(message);
writer.flush();
String currentTime = now().format(ofLocalizedTime(FormatStyle.MEDIUM));
System.out.println(currentTime + " Sent " + message);
TimeUnit.SECONDS.sleep(1);
}
} catch (IOException | InterruptedException e) {
e.printStackTrace();
}
}
}
```

I can help you make your multithreaded code more predictableThread.sleep(), CountDownLatch I represent a job to run Runnable I store the IP address and port of the server InetSocketAddress (from pages 634–635) You should get the same output even if you move the sleep() to somewhere else inside this for loop. You can catch the InterruptedException thrown by sleep() inside the for loop, or you can catch all the Exceptions at the end of the method.

## Code Kitchen

## Code Kitchen