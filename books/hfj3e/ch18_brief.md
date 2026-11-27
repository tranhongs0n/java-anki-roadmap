# Chapter 18: Chapter 18: Dealing with Concurrency Issues

pages 677-710

easy. Writing multithreaded code that works the way you expect can be much harder. In this final chapter, we’re going to show you some of the things that can go wrong when two or more threads are working at the same time. You’ll learn about some of the tools in java.util.concurrent that can help you to write multithreaded code that works correctly. You’ll learn how to create immutable objects (objects that don’t change) that are safe for multiple threads to use. By the

end of the chapter, you’ll have a lot of different tools in your toolkit for working with concurrency. this is a new chapter concurrency issues

## What could possibly go wrong?

At the end of the last chapter we hinted that things may not all be rainbows and sunshine when you’re working with multithreaded code. Well, actually, we did more than hint! We outright said: Shared object “It all comes down to one potentially deadly scenario: two or more threads have access to a single object’s data.” A B writing writing writing writing writing reading reading reading These two threads are merrily reading

## The Ryan and Monica problem, in code

```java
RyanAndMonicaJob ryan = new RyanAndMonicaJob("Ryan", account, 50);
RyanAndMonicaJob monica = new RyanAndMonicaJob("Monica", account, 100);
```

```java
if (account.getBalance() >= amount) {
account.spend(amount);
} else {
System.out.println("Sorry, not enough money");
}
```

```java
BankAccount account = new BankAccount();
ExecutorService executor = Executors.newFixedThreadPool(2);
executor.execute(ryan);
executor.execute(monica);
```

```java
import java.util.concurrent.*;
public class RyanAndMonicaTest {
public static void main(String[] args) {
BankAccount account = new BankAccount();
RyanAndMonicaJob ryan = new RyanAndMonicaJob("Ryan", account, 50);
RyanAndMonicaJob monica = new RyanAndMonicaJob("Monica", account, 100);
ExecutorService executor = Executors.newFixedThreadPool(2);
executor.execute(ryan);
executor.execute(monica);
executor.shutdown();
}
}
class RyanAndMonicaJob implements Runnable {
private final String name;
private final BankAccount account;
private final int amountToSpend;
RyanAndMonicaJob(String name, BankAccount account, int amountToSpend) {
this.name = name;
this.account = account;
this.amountToSpend = amountToSpend;
}
public void run() {
goShopping(amountToSpend);
}
private void goShopping(int amount) {
if (account.getBalance() >= amount) {
System.out.println(name + " is about to spend");
account.spend(amount);
System.out.println(name + " finishes spending");
} else {
System.out.println("Sorry, not enough for " + name);
}
}
}
class BankAccount {
private int balance = 100;
public int getBalance() {
return balance;
}
public void spend(int amount) {
balance = balance - amount;
if (balance < 0) {
System.out.println("Overdrawn!");
}
}
}
```

```java
% java RyanAndMonicaTest
Ryan is about to spend
Monica is about to spend
Overdrawn!
Ryan finishes spending
Monica finishes spending
```

```java
% java RyanAndMonicaTest
Ryan is about to spend
Ryan finishes spending
Sorry, not enough for Monica
```

## They need a lock for account access!

```java
private void goShopping(int amount) {
synchronized (account) {
if (account.getBalance() >= amount) {
System.out.println(name + " is about to spend");
account.spend(amount);
System.out.println(name + " finishes spending");
} else {
System.out.println("Sorry, not enough for " + name);
}
}
}
```

## Using an object’s lock

## Using synchronized methods

```java
% java RyanAndMonicaTest
Ryan is about to spend
Ryan finishes spending
Monica is about to spend
Overdrawn!
Monica finishes spending
private synchronized void goShopping(int amount) {
if (account.getBalance() >= amount) {
System.out.println(name + " is about to spend");
account.spend(amount);
System.out.println(name + " finishes spending");
} else {
System.out.println("Sorry, not enough for " + name);
}
}
```

## It’s important to lock the correct object

```java
class RyanAndMonicaJob implements Runnable {
// ...rest of the RyanAndMonicaJob class
// the same as before...
private void goShopping(int amount) {
System.out.println(name + " is about to spend");
account.spend(name, amount);
System.out.println(name + " finishes spending");
}
}
class BankAccount {
// other methods in BankAccount...
public synchronized void spend(String name, int amount) {
if (balance >= amount) {
balance = balance - amount;
if (balance < 0) {
System.out.println("Overdrawn!");
}
} else {
System.out.println("Sorry, not enough for " + name);
}
}
}
```

Since it’s the BankAccount object that’s shared, you could argue it should be the BankAccount that’s in charge of making sure it is safe for multiple threads to use. The spend() method on BankAccount could make sure there’s enough money and debit the account in a single transaction. This would no longer need to check the balance before spending if we know the BankAccount spend() method checks for us.

## The dreaded “Lost Update” problem

```java
int i = balance;
```

```java
balance = i + 1;
```

Here’s another classic concurrency problem. Sometimes you’ll hear them called “race conditions,” where two or more threads are changing the same data at the same time. It’s closely related to the Ryan and Monica story, so we’ll use this example to illustrate a few more points. The lost update revolves around one process: Step 1: Get the balance in the account Step 2: Add 1 to that balance Even if we used the more common syntax of balance++, there is no guarantee that the compiled bytecode will be an “atomic process.” In fact, it probably won’t—it’s actually multiple operations: a read of the current value and then adding one to that value and setting it back into the original variable.

```java
public class LostUpdate {
public static void main(String[] args) throws InterruptedException {
ExecutorService pool = Executors.newFixedThreadPool(6);
Balance balance = new Balance();
for (int i = 0; i < 1000; i++) {
pool.execute(() -> balance.increment());
}
pool.shutdown();
if (pool.awaitTermination(1, TimeUnit.MINUTES)) {
System.out.println("balance = " + balance.balance);
}
}
}
class Balance {
int balance = 0;
public void increment() {
balance++;
}
}
```

In the “Lost Update” problem, we have many threads trying to increment the balance. Take a look at the code, and then we’ll look at the real problem: Probably not an atomic process Create a thread pool to run all the jobs. If you add more threads here, you may see even more missing updates. Run 1,000 attempts to update the balance, on different threads. Here’s the crucial part! We increment the balance by adding 1 to whatever the value of balance was AT THE TIME WE READ IT (rather than adding 1 to whatever the CURRENT value is). You might think that “++” is an atomic operation, but it is not.

## Let’s run this code...

```java
public synchronized void increment() {
balance++;
}
```

```java
public void go() {
doStuff();
synchronized(this) {
criticalStuff();
moreCriticalStuff();
}
}
```

## Deadlock, a deadly side of synchronization

## You don’t always have to use synchronized

Since synchronization can come with some costs (like performance and potential deadlocks), you should know about other ways to manage data that’s shared between threads. The java.util.concurrent package has lots of classes and utilities for working with multithreaded code. Atomic variables If the shared data is an int, long, or boolean, we might be able to replace it with an atomic variable. These classes provide methods that are atomic, i.e., can safely be used by a thread without worrying about another thread changing the object’s values at the same time.

```java
class Balance {
AtomicInteger balance = new AtomicInteger(0);
public void increment() {
balance.incrementAndGet();
}
}
```

Since Ryan and Monica were both trying to access an int value, the account balance, we could use an AtomicInteger to store that balance. We could then use compareAndSet to update the balance when someone wants to spend money.

## Compare-and-swap with atomic variables

```java
private AtomicInteger balance = new AtomicInteger(100);
...
boolean success = balance.compareAndSet(expectedValue, newValue)
```

```java
import java.util.concurrent.atomic.AtomicInteger;
class BankAccount {
private final AtomicInteger balance = new AtomicInteger(100);
public int getBalance() {
return balance.get();
}
public void spend(String name, int amount) {
int initialBalance = balance.get();
if (initialBalance >= amount) {
boolean success = balance.compareAndSet(initialBalance, initialBalance - amount);
if (!success) {
System.out.println("Sorry " + name + ", you haven't spent the money.");
}
} else {
System.out.println("Sorry, not enough for " + name);
}
}
}
```

Let’s see the whole thing in action in Ryan and Monica’s bank account. We’ll put the balance in an AtomicInteger and use compareAndSet to make an atomic change to the balance. The balance will NOT be changed if the initial balance does not match the actual balance right now. If success was false, the money was NOT spent. Tell Ryan or Monica it didn’t work and they can decide what to do.

## Ryan and Monica, going atomic

```java
% java RyanAndMonicaTest
Ryan is about to spend
Monica is about to spend
Ryan finishes spending
Sorry Monica, you can’t buy this
Monica finishes spending
```

## Writing a class for immutable data

```java
public final class ImmutableData {
private final String name;
private final int value;
public ImmutableData(String name, int value) {
this.name = name;
this.value = value;
}
public String getName() { return name; }
public int getValue() { return value; }
}
```

## Using immutable objects

## Changing immutable data

## More problems with shared data

```java
public class ConcurrentReaders {
public static void main(String[] args) {
List<Chat> chatHistory = new ArrayList<>();
ExecutorService executor = Executors.newFixedThreadPool(3);
for (int i = 0; i < 5; i++) {
executor.execute(() -> chatHistory.add(new Chat("Hi there!")));
executor.execute(() -> System.out.println(chatHistory));
executor.execute(() -> System.out.println(chatHistory));
}
executor.shutdown();
}
}
final class Chat {
private final String message;
private final LocalDateTime timestamp;
public Chat(String message) {
this.message = message;
timestamp = LocalDateTime.now();
}
public String toString() {
String time = timestamp.format(ofLocalizedTime(MEDIUM));
return time + " " + message;
}
}
```

```java
% java ConcurrentReaders
[]
[]
[18:43:59 Hi there!, 18:43:59 Hi there!]
[18:43:59 Hi there!, 18:43:59 Hi there!]
[18:43:59 Hi there!, 18:43:59 Hi there!, 18:43:59 Hi there!]
[18:43:59 Hi there!, 18:43:59 Hi there!, 18:43:59 Hi there!]
Exception in thread "pool-1-thread-2" Exception in thread "pool-1-thread-1" java.util.
ConcurrentModificationException
at java.base/java.util.ArrayList$Itr.checkForComodification(ArrayList.java:1043)
at java.base/java.util.ArrayList$Itr.next(ArrayList.java:997)
at java.base/java.util.AbstractCollection.toString(AbstractCollection.java:472)
at java.base/java.lang.String.valueOf(String.java:2951)
at java.base/java.io.PrintStream.println(PrintStream.java:897)
at ConcurrentReaders.lambda$main$2(ConcurrentReaders.java:17)
```

## Use a thread-safe data structure

Clearly good ol’ ArrayList just isn’t going to cut it if you have threads reading data that’s being changed at the same time. Luckily for us, there are other options. We want a thread-safe data structure, one that can be written to, and read from, by multiple threads at the same time. The java.util.concurrent package has a number of thread-safe data structures, and we’re going to look at CopyOnWriteArrayList to solve this specific problem.

```java
public class ConcurrentReaders {
public static void main(String[] args) {
List<Chat> chatHistory = new CopyOnWriteArrayList<>();
ExecutorService executor = Executors.newFixedThreadPool(3);
for (int i = 0; i < 5; i++) {
executor.execute(() -> chatHistory.add(new Chat("Hi there!")));
executor.execute(() -> System.out.println(chatHistory));
executor.execute(() -> System.out.println(chatHistory));
}
executor.shutdown();
}
}
```

```java
% java ConcurrentReaders
[]
[]
[]
[]
[10:26:22 Hi there!, 10:26:22 Hi there!]
[10:26:22 Hi there!, 10:26:22 Hi there!, 10:26:22 Hi there!, 10:26:22 Hi there!]
[10:26:22 Hi there!, 10:26:22 Hi there!, 10:26:22 Hi there!]
[10:26:22 Hi there!, 10:26:22 Hi there!, 10:26:22 Hi there!, 10:26:22 Hi there!]
[10:26:22 Hi there!, 10:26:22 Hi there!, 10:26:22 Hi there!, 10:26:22 Hi there!, 10:26:22 Hi there!]
[10:26:22 Hi there!, 10:26:22 Hi there!, 10:26:22 Hi there!, 10:26:22 Hi there!, 10:26:22 Hi there!]
Process finished with exit code 0
```

## CopyOnWriteArrayList

CopyOnWriteArrayList uses immutability to provide safe access for reading threads while other threads are writing. How does it work? Well, it does what it says on the tin: when a thread is writing to the list, it’s actually writing to a copy of the list. When the changes have been made, then the new copy replaces the original. In the meantime, any threads that were reading the list before the change are happily (and safely!) reading the original.

```java
import java.util.*;
import java.util.concurrent.*;
public class TwoThreadsWriting {
public static void main(String[] args) {
ExecutorService threadPool = Executors.newFixedThreadPool(2);
Data data = new Data();
threadPool.execute(() -> addLetterToData('a', data));
threadPool.execute(() -> addLetterToData('A', data));
threadPool.shutdown();
}
private static void addLetterToData(char letter, Data data) {
for (int i = 0; i < 26; i++) {
data.addLetter(letter++);
try {
Thread.sleep(50);
} catch (InterruptedException ignored) {}
}
System.out.println(Thread.currentThread().getName() + data.getLetters());
System.out.println(Thread.currentThread().getName()
+ " size = " + data.getLetters().size());
}
}
final class Data {
private final List<String> letters = new ArrayList<>();
public List<String> getLetters() {return letters;}
public void addLetter(char letter) {
letters.add(String.valueOf(letter));
}
}
```

portal at sunrise over the Indian Ocean. Even though the ship’s conference room was incredibly claustrophobic, the sight of the growing blue and white crescent overtaking night on the planet below filled Sarah with awe and appreciation. This morning’s meeting was focused on the control systems for the orbiter’s airlocks. As the final construction phases were nearing their end, the number of spacewalks was scheduled

to increase dramatically, and traffic was high both in and out of the ship’s airlocks. “Good morning, Sarah,” said Tom, “Your timing is perfect; we’re just starting the detailed design review.” “As you all know,” said Tom, “Each airlock is outfitted with space-hardened GUI terminals, both inside and out. Whenever spacewalkers are entering or exiting the orbiter they will use these terminals to initiate the airlock sequences.” Sarah nodded and asked, “Tom, can you tell us what the method sequences are for entry and exit?” Tom rose and floated to the whiteboard, “First, here’s the exit sequence method’s pseudocode.” Tom quickly wrote on the board.

```java
orbiterAirlockExitSequence()
verifyPortalStatus();
pressurizeAirlock();
openInnerHatch();
confirmAirlockOccupied();
closeInnerHatch();
decompressAirlock();
openOuterHatch();
confirmAirlockVacated();
```

```java
% java TwoThreadsWriting
pool-1-thread-2[a, A, b, B, c, C, d, D, E, F, g, G, h, H, i, j, K, k,
pool-1-thread-1[a, A, b, B, c, C, d, D, E, F, g, G, h, H, i, j, K, k,
pool-1-thread-1 size = 40
pool-1-thread-2 size = 40
```

and it finally clicked as Tom began to write the entry sequence pseudocode on the whiteboard. “Wait a minute, Tom!” cried Sarah, “I think we’ve got a big flaw in the exit sequence design. Let’s go back and revisit it; it could be critical!” Why did Sarah stop the meeting? What did she suspect? Five-Minute Mystery Near-miss at the airlock Answers on page 671. File Edit Window Help ZeCount BE the JVM (from page 668)

```java
public synchronized void addLetter(char letter) {
letters.add(String.valueOf(letter));
}
```

```java
private final List<String> letters = new CopyOnWriteArrayList<>();
```