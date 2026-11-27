# 12. Error Handling with Exceptions (printed p313-354)


<!--p335-->

<!--p336-->
Error Handling with Exceptions The basic philosophy of Java is that "badly formed code will not be run." The ideal time to catch an error is at compile time, before you even try to run the program. However, not all errors can be detected at compile time. The rest of the problems must be handled at run time through some formality that allows the originator of the error to pass appropriate information to a recipient who will know how to handle the difficulty properly. Improved error recovery is one of the most powerful ways that you can increase the robustness of your code. Error recovery is a fundamental concern for every program you write, but it’s especially important in Java, where one of the primary goals is to create program components for others to use. To create a robust system, each component must be robust. By providing a consistent error-reporting model using exceptions, Java allows components to reliably communicate problems to client code. The goals for exception handling in Java are to simplify the creation of large, reliable programs using less code than currently possible, and to do so with more confidence that your application doesn’t have an unhandled error. Exceptions are not terribly difficult to learn, and are one of those features that provide immediate and significant benefits to your project. Because exception handling is the only official way that Java reports errors, and it is enforced by the Java compiler, there are only so many examples that can be written in this book without learning about exception handling. This chapter introduces you to the code that you need to write to properly handle exceptions, and shows how you can generate your own exceptions if one of your methods gets into trouble. Concepts C and other earlier languages often had multiple error-handling schemes, and these were generally established by convention and not as part of the programming language. Typically, you returned a special value or set a flag, and the recipient was supposed to look at the value or the flag and determine that something was amiss. However, as the years passed, it was discovered that programmers who use a library tend to think of themselves as invincible—as in "Yes, errors might happen to others, but not in my code." So, not too surprisingly, they wouldn’t check for the error conditions (and sometimes the error conditions were too silly to check for1). If you were thorough enough to check for an error every time you called a method, your code could turn into an unreadable nightmare. Because programmers could still coax systems out of these languages, they were resistant to admitting the truth: that this approach to handling errors was a major limitation to creating large, robust, maintainable programs. The solution is to take the casual nature out of error handling and to enforce formality. This actually has a long history, because implementations of exception handling go back to operating systems in the 1960s, and even to BASIC’S "on error goto."But C++ exception 1The C programmer can look up the return value of printf( ) for an example of this. handling was based on Ada, and Java’s is based primarily on C++ (although it looks more like Object Pascal). The word "exception" is meant in the sense of "I take exception to that." At the point where the problem occurs, you might not know what to do with it, but you do know that you can’t just continue on merrily; you must stop, and somebody, somewhere, must figure out what to do. But you don’t have enough information in the current context to fix the problem. So you hand the problem out to a higher context where someone is qualified to make the proper decision. The other rather significant benefit of exceptions is that they tend to reduce the complexity of error-handling code. Without exceptions, you must check for a particular error and deal with it at multiple places in your program. With exceptions, you no longer need to check for errors at the point of the method call, since the exception will guarantee that someone catches it. You only need to handle the problem in one place, in the so-called exception handler. This saves you code, and it separates the code that describes what you want to do during normal execution from the code that is executed when things go awry. In general, reading, writing, and debugging code becomes much clearer with exceptions than when using the old way of error handling. Basic exceptions An exceptional condition is a problem that prevents the continuation of the current method or scope. It’s important to distinguish an exceptional condition from a normal problem, in which you have enough information in the current context to somehow cope with the difficulty. With an exceptional condition, you cannot continue processing because you don’t have the information necessary to deal with the problem in the current context. All you can do is jump out of the current context and relegate that problem to a higher context. This is what happens when you throw an exception. Division is a simple example. If you’re about to divide by zero, it’s worth checking for that condition. But what does it mean that the denominator is zero? Maybe you know, in the context of the problem you’re trying to solve in that particular method, how to deal with a zero denominator. But if it’s an unexpected value, you can’t deal with it and so must throw an exception rather than continuing along that execution path. When you throw an exception, several things happen. First, the exception object is created in the same way that any Java object is created: on the heap, with new. Then the current path of execution (the one you couldn’t continue) is stopped and the reference for the exception object is ejected from the current context. At this point the exception-handling mechanism takes over and begins to look for an appropriate place to continue executing the program. This appropriate place is the exception handler, whose job is to recover from the problem so the program can either try another tack or just continue. As a simple example of throwing an exception, consider an object reference called t. It’s possible that you might be passed a reference that hasn’t been initialized, so you might want to check before trying to call a method using that object reference. You can send information about the error into a larger context by creating an object representing your information and "throwing" it out of your current context. This is called throwing an exception. Here’s what it looks like:
```java
if(t == null)
throw new NullPointerException();
```

<!--p337-->
This throws the exception, which allows you—in the current context—to abdicate responsibility for thinking about the issue further. It’s just magically handled somewhere else. Precisely where will be shown shortly. Error Handling with Exceptions Exceptions allow you to think of everything that you do as a transaction, and the exceptions guard those transactions: "...the fundamental premise of transactions is that we needed exception handling in distributed computations. Transactions are the computer equivalent of contract law. If anything goes wrong, we’ll just blow away the whole computation."2You can also think about exceptions as a built-in undo system, because (with some care) you can have various recovery points in your program. If a part of the program fails, the exception will "undo" back to a known stable point in the program. One of the most important aspects of exceptions is that if something bad happens, they don’t allow a program to continue along its ordinary path. This has been a real problem in languages like C and C++; especially C, which had no way to force a program to stop going down a path if a problem occurred, so it was possible to ignore problems for a long time and get into a completely inappropriate state. Exceptions allow you to (if nothing else) force the program to stop and tell you what went wrong, or (ideally) force the program to deal with the problem and return to a stable state. Exception arguments As with any object in Java, you always create exceptions on the heap using new, which allocates storage and calls a constructor. There are two constructors in all standard exceptions: The first is the default constructor, and the second takes a string argument so that you can place pertinent information in the exception:
```java
throw new NullPointerException("t = null");
```

<!--p338-->
This string can later be extracted using various methods, as you’ll see. The keyword throw produces a number of interesting results. After creating an exception object with new, you give the resulting reference to throw. The object is, in effect, "returned" from the method, even though that object type isn’t normally what the method is designed to return. A simplistic way to think about exception handling is as a different kind of return mechanism, although you get into trouble if you take that analogy too far. You can also exit from ordinary scopes by throwing an exception. In either case, an exception object is returned, and the method or scope exits. Any similarity to an ordinary return from a method ends here, because where you return is someplace completely different from where you return for a normal method call. (You end up in an appropriate exception handler that might be far away—many levels on the call stack— from where the exception was thrown.) In addition, you can throw any type of Throwable, which is the exception root class. Typically, you’ll throw a different class of exception for each different type of error. The information about the error is represented both inside the exception object and implicitly in the name of the exception class, so someone in the bigger context can figure out what to do with your exception. (Often, the only information is the type of exception, and nothing meaningful is stored within the exception object.) Catching an exception To see how an exception is caught, you must first understand the concept of a guarded region. This is a section of code that might produce exceptions and is followed by the code to handle those exceptions. 2Jim Gray, Turing Award winner for his team’s contributions on transactions, in an interview on www.acmqueue.org.
## The try block
If you’re inside a method and you throw an exception (or another method that you call within this method throws an exception), that method will exit in the process of throwing. If you don’t want a throw to exit the method, you can set up a special block within that method to capture the exception. This is called the try block because you "try" your various method calls there. The try block is an ordinary scope preceded by the keyword try:
```java
try {
// Code that might generate exceptions
}
```
If you were checking for errors carefully in a programming language that didn’t support exception handling, you’d have to surround every method call with setup and error-testing code, even if you call the same method several times. With exception handling, you put everything in a try block and capture all the exceptions in one place. This means your code is much easier to write and read because the goal of the code is not confused with the error checking. Exception handlers Of course, the thrown exception must end up someplace. This "place" is the exception handler, and there’s one for every exception type you want to catch. Exception handlers immediately follow the try block and are denoted by the keyword catch:
```java
try {
// Code that might generate exceptions
} catch(Type1 id1)|{
// Handle exceptions of Type1
} catch(Type2 id2) {
// Handle exceptions of Type2
} catch(Type3 id3) {
// Handle exceptions of Type3
}
// etc...
```

<!--p339-->
Each catch clause (exception handler) is like a little method that takes one and only one argument of a particular type. The identifier (id1, id2, and so on) can be used inside the handler, just like a method argument. Sometimes you never use the identifier because the type of the exception gives you enough information to deal with the exception, but the identifier must still be there. The handlers must appear directly after the try block. If an exception is thrown, the exception-handling mechanism goes hunting for the first handler with an argument that matches the type of the exception. Then it enters that catch clause, and the exception is considered handled. The search for handlers stops once the catch clause is finished. Only the matching catch clause executes; it’s not like a switch statement in which you need a break after each case to prevent the remaining ones from executing. Note that within the try block, a number of different method calls might generate the same exception, but you need only one handler. Error Handling with Exceptions Termination vs. resumption There are two basic models in exception-handling theory. Java supportst termination,3in which you assume that the error is so critical that there’s no way to get back to where the exception occurred. Whoever threw the exception decided that there was no way to salvage the situation, and they don’t want to come back. The alternative is called resumption. It means that the exception handler is expected to do something to rectify the situation, and then the faulting method is retried, presuming success the second time. If you want resumption, it means you still hope to continue execution after the exception is handled. If you want resumption-like behavior in Java, don’t throw an exception when you encounter an error. Instead, call a method that fixes the problem. Alternatively, place your try block inside a while loop that keeps reentering the try block until the result is satisfactory. Historically, programmers using operating systems that supported resumptive exception handling eventually ended up using termination-like code and skipping resumption. So although resumption sounds attractive at first, it isn’t quite so useful in practice. The dominant reason is probably the coupling that results: A resumptive handler would need to be aware of where the exception is thrown, and contain non-generic code specific to the throwing location. This makes the code difficult to write and maintain, especially for large systems where the exception can be generated from many points. Creating your own exceptions You’re not stuck using the existing Java exceptions. The Java exception hierarchy can’t foresee all the errors you might want to report, so you can create your own to denote a special problem that your library might encounter. To create your own exception class, you must inherit from an existing exception class, preferably one that is close in meaning to your new exception (although this is often not possible). The most trivial way to create a new type of exception is just to let the compiler create the default constructor for you, so it requires almost no code at all:
```java
//: exceptions/InheritingExceptions.java
// Creating your own exceptions.
class SimpleException extends Exception {}
public class InheritingExceptions {
public void f() throws SimpleException {
System.out.println("Throw SimpleException from f()");
throw new SimpleException();
}
public static void main(String[] args) {
InheritingExceptions sed = new InheritingExceptions();
try {
sed.f();
} catch(SimpleException e) {
System.out.println("Caught it!");
}
}
} /* Output:
Throw SimpleException from f()
```

<!--p340-->
3As do most languages, including C++, C#, Python, D, etc.
```java
Caught it!
*///:~
```
The compiler creates a default constructor, which automatically (and invisibly) calls the base- class default constructor. Of course, in this case you don’t get a SimpleException(String) constructor, but in practice that isn’t used much. As you’ll see, the most important thing about an exception is the class name, so most of the time an exception like the one shown here is satisfactory. Here, the result is printed to the console, where it is automatically captured and tested with this book’s output-display system. However, you may want to send error output to the standard error stream by writing to System.err. This is usually a better place to send error information than System.out, which may be redirected. If you send output to System.err, it will not be redirected along with System.out so the user is more likely to notice it. You can also create an exception class that has a constructor with a String argument:
```java
//: exceptions/FullConstructors.java
class MyException extends Exception {
public MyException() {}
public MyException(String msg) { super(msg); }
}
public class FullConstructors {
public static void f() throws MyException {
System.out.println("Throwing MyException from f()");
throw new MyException();
}
public static void g() throws MyException {
System.out.println("Throwing MyException from g()");
throw new MyException("Originated in g()");
}
public static void main(String[] args) {
try {
f();
} catch(MyException e) {
e.printStackTrace(System.out);
}
try {
g();
} catch(MyException e) {
e.printStackTrace(System.out);
}
}
} /* Output:
Throwing MyException from f()
MyException
at FullConstructors.f(FullConstructors.java:11)
at FullConstructors.main(FullConstructors.java:19)
Throwing MyException from g()
MyException: Originated in g()
at FullConstructors.g(FullConstructors.java:15)
at FullConstructors.main(FullConstructors.java:24)
*///:~
```

<!--p341-->
The added code is small: two constructors that define the way MyException is created. In the second constructor, the base-class constructor with a String argument is explicitly invoked by using the super keyword. In the handlers, one of the Throwable (from which Exception is inherited) methods is called: printStackTrace( ). As you can see from the output, this produces information about the sequence of methods that were called to get to the point where the exception happened. Here, the information is sent to System.out, and automatically captured and displayed in the output. However, if you call the default version:
```java
e.printStackTrace();
```
the information goes to the standard error stream. Exercise 1:(2) Create a class with a main( ) that throws an object of class Exception inside a try block. Give the constructor for Exception a String argument. Catch the exception inside a catch clause and print the String argument. Add a finally clause and print a message to prove you were there. Exercise 2:(1) Define an object reference and initialize it to null. Try to call a method through this reference. Now wrap the code in a try-catch clause to catch the exception. Exercise 3:(1) Write code to generate and catch an ArraylndexOutOfBoundsException. Exercise 4:(2) Create your own exception class using the extends keyword. Write a constructor for this class that takes a String argument and stores it inside the object with a String reference. Write a method that displays the stored String. Create a try-catch clause to exercise your new exception. Exercise 5:(3) Create your own resumption-like behavior using a while loop that repeats until an exception is no longer thrown. Exceptions and logging You may also want to log the output using the java.util.logging facility. Although full details of logging are introduced in the supplement at http://MindView.net/Books/BetterJava, basic logging is straightforward enough to be used here.
```java
//: exceptions/LoggingExceptions.java
// An exception that reports through a Logger.
import java.util.logging.*;
import java.io.*;
class LoggingException extends Exception {
private static Logger logger =
Logger.getLogger("LoggingException");
public LoggingException() {
StringWriter trace = new StringWriter();
printStackTrace(new PrintWriter(trace));
logger.severe(trace.toString());
}
}
public class LoggingExceptions {
public static void main(String[] args) {
try {
throw new LoggingException();
} catch(LoggingException e) {
System.err.println("Caught " + e);
}
try {
throw new LoggingException();
```

<!--p342-->
Error Handling with Exceptions
```java
} catch(LoggingException e) {
System.err.println("Caught " + e);
}
}
} /* Output: (85% match)
Aug 30, 2005 4:02:31 PM LoggingException <init>
SEVERE: LoggingException
at LoggingExceptions.main(LoggingExceptions.java:19)
Caught LoggingException
Aug 30, 2005 4:02:31 PM LoggingException <init>
SEVERE: LoggingException
at LoggingExceptions.main(LoggingExceptions.java:24)
Caught LoggingException
*///:~
```
The static Logger.getLogger( ) method creates a Logger object associated with the String argument (usually the name of the package and class that the errors are about) which sends its output to System.err. The easiest way to write to a Logger is just to call the method associated with the level of logging message; here, severe( ) is used. To produce the String for the logging message, we’d like to have the stack trace where the exception is thrown, but printStackTrace( ) doesn’t produce a String by default. To get a String, we need to use the overloaded printStackTrace( ) that takes a java.io.PrintWriter object as an argument (all of this will be fully explained in the I/O chapter). If we hand the Print Writer constructor a java.io.StringWriter object, the output can be extracted as a String by calling toString( ). Although the approach used by LoggingException is very convenient because it builds all the logging infrastructure into the exception itself, and thus it works automatically without client programmer intervention, it’s more common that you will be catching and logging someone else’s exception, so you must generate the log message in the exception handler:
```java
//: exceptions/LoggingExceptions2.java
// Logging caught exceptions.
import java.util.logging.*;
import java.io.*;
public class LoggingExceptions2 {
private static Logger logger =
Logger.getLogger("LoggingExceptions2");
static void logException(Exception e) {
StringWriter trace = new StringWriter();
e.printStackTrace(new PrintWriter(trace));
logger.severe(trace.toString());
}
public static void main(String[] args) {
try {
throw new NullPointerException();
} catch(NullPointerException e) {
logException(e);
}
}
} /* Output: (90% match)
Aug 30, 2005 4:07:54 PM LoggingExceptions2 logException
SEVERE: java.lang.NullPointerException
at LoggingExceptions2.main(LoggingExceptions2.java:16)
*///:~
```

<!--p343-->
The process of creating your own exceptions can be taken further. You can add extra constructors and members:
```java
//: exceptions/ExtraFeatures.java
// Further embellishment of exception classes.
import static net.mindview.util.Print.*;
class MyException2 extends Exception {
private int x;
public MyException2() {}
public MyException2(String msg) { super(msg); }
public MyException2(String msg, int x) {
super(msg);
this.x = x;
}
public int val() { return x; }
public String getMessage() {
return "Detail Message: "+ x + " "+ super.getMessage();
}
}
public class ExtraFeatures {
public static void f() throws MyException2 {
print("Throwing MyException2 from f()");
throw new MyException2();
}
public static void g() throws MyException2 {
print("Throwing MyException2 from g()");
throw new MyException2("Originated in g()");
}
public static void h() throws MyException2 {
print("Throwing MyException2 from h()");
throw new MyException2("Originated in h()", 47);
}
public static void main(String[] args) {
try {
f();
} catch(MyException2 e) {
e.printStackTrace(System.out);
}
try {
g();
} catch(MyException2 e) {
e.printStackTrace(System.out);
}
try {
h();
} catch(MyException2 e) {
e.printStackTrace(System.out);
System.out.println("e.val() = " + e.val());
}
}
} /* Output:
Throwing MyException2 from f()
MyException2: Detail Message: 0 null
at ExtraFeatures.f(ExtraFeatures.java:22)
at ExtraFeatures.main(ExtraFeatures.java:34)
Throwing MyException2 from g()
MyException2: Detail Message: 0 Originated in g()
at ExtraFeatures.g(ExtraFeatures.java:26)
at ExtraFeatures.main(ExtraFeatures.java:39)
Throwing MyException2 from h()
MyException2: Detail Message: 47 Originated in h()
at ExtraFeatures.h(ExtraFeatures.java:30)
at ExtraFeatures.main(ExtraFeatures.java:44)
e.val() = 47
```

<!--p344-->
Error Handling with Exceptions
```java
*///:~
```
A field x has been added, along with a method that reads that value and an additional constructor that sets it. In addition, Throwable.getMessage( ) has been overridden to produce a more interesting detail message. getMessage( ) is something like toString( ) for exception classes. Since an exception is just another kind of object, you can continue this process of embellishing the power of your exception classes. Keep in mind, however, that all this dressing-up might be lost on the client programmers using your packages, since they might simply look for the exception to be thrown and nothing more. (That’s the way most of the Java library exceptions are used.) Exercise 6:(1) Create two exception classes, each of which performs its own logging automatically. Demonstrate that these work. Exercise 7: (1) Modify Exercise 3 so that the catch clause logs the results. The exception specification In Java, you’re encouraged to inform the client programmer, who calls your method, of the exceptions that might be thrown from your method. This is civilized, because the caller can then know exactly what code to write to catch all potential exceptions. Of course, if the source code is available, the client programmer could hunt through and look for throw statements, but a library might not come with sources. To prevent this from being a problem, Java provides syntax (and forces you to use that syntax) to allow you to politely tell the client programmer what exceptions this method throws, so the client programmer can handle them. This is the exception specification and it’s part of the method declaration, appearing after the argument list. The exception specification uses an additional keyword, throws, followed by a list of all the potential exception types. So your method definition might look like this:
```java
void f() throws TooBig, TooSmall, DivZero { //...
```
However, if you say
```java
void f() { //...
```

<!--p345-->
it means that no exceptions are thrown from the method {except for the exceptions inherited from RuntimeException, which can be thrown anywhere without exception specifications—these will be described later). You can’t lie about an exception specification. If the code within your method causes exceptions, but your method doesn’t handle them, the compiler will detect this and tell you that you must either handle the exception or indicate with an exception specification that it may be thrown from your method. By enforcing exception specifications from top to bottom, Java guarantees that a certain level of exception correctness can be ensured at compile time. There is one place you can lie: You can claim to throw an exception that you really don’t. The compiler takes your word for it, and forces the users of your method to treat it as if it really does throw that exception. This has the beneficial effect of being a placeholder for that exception, so you can actually start throwing the exception later without requiring changes to existing code. It’s also important for creating abstract base classes and interfaces whose derived classes or implementations may need to throw exceptions. Exceptions that are checked and enforced at compile time are called checked exceptions. Exercise 8:(1) Write a class with a method that throws an exception of the type created in Exercise 4. Try compiling it without an exception specification to see what the compiler says. Add the appropriate exception specification. Try out your class and its exception inside a try-catch clause. Catching any exception It is possible to create a handler that catches any type of exception. You do this by catching the base-class exception type Exception (there are other types of base exceptions, but Exception is the base that’s pertinent to virtually all programming activities):
```java
catch(Exception e) {
System.out.println("Caught an exception");
}
```
This will catch any exception, so if you use it you’ll want to put it at the end of your list of handlers to avoid preempting any exception handlers that might otherwise follow it. Since the Exception class is the base of all the exception classes that are important to the programmer, you don’t get much specific information about the exception, but you can call the methods that come from its base type Throwable: String getMessage( ) String getLocalizedMessage( ) Gets the detail message, or a message adjusted for this particular locale. String toString( ) Returns a short description of the Throwable, including the detail message if there is one. void printStackTrace( ) voidprintStackTrace(PrintStream) voidprintStackTrace(java.io.PrintWriter) Prints the Throwable and the Throwable’scall stack trace. The call stack shows the sequence of method calls that brought you to the point at which the exception was thrown. The first version prints to standard error, the second and third print to a stream of your choice (in the I/O chapter, you’ll understand why there are two types of streams). Throwable fillInStackTrace( ) Records information within this Throwable object about the current state of the stack frames. Useful when an application is rethrowing an error or exception (more about this shortly). In addition, you get some other methods from Throwable’sbase type Object (everybody’s base type). The one that might come in handy for exceptions is getClass( ), which returns an object representing the class of this object. You can in turn query this Class object for its name with getName( ), which includes package information, or getSimpleName( ), which produces the class name alone. Here’s an example that shows the use of the basic Exception methods:
```java
//: exceptions/ExceptionMethods.java
// Demonstrating the Exception Methods.
import static net.mindview.util.Print.*;
```

<!--p346-->
Error Handling with Exceptions
```java
public class ExceptionMethods {
public static void main(String[] args) {
try {
throw new Exception("My Exception");
} catch(Exception e) {
print("Caught Exception");
print("getMessage():" + e.getMessage());
print("getLocalizedMessage():" +
e.getLocalizedMessage());
print("toString():" + e);
print("printStackTrace():");
e.printStackTrace(System.out);
}
}
} /* Output:
Caught Exception
getMessage():My Exception
getLocalizedMessage():My Exception
toString():java.lang.Exception: My Exception
printStackTrace():
java.lang.Exception: My Exception
at ExceptionMethods.main(ExceptionMethods.java:8)
*///:~
```
You can see that the methods provide successively more information—each is effectively a superset of the previous one. Exercise 9:(2) Create three new types of exceptions. Write a class with a method that throws all three. In main( ), call the method but only use a single catch clause that will catch all three types of exceptions. The stack trace The information provided by printStackTrace( ) can also be accessed directly using getStackTrace( ). This method returns an array of stack trace elements, each representing one stack frame. Element zero is the top of the stack, and is the last method invocation in the sequence (the point this Throwable was created and thrown). The last element of the array and the bottom of the stack is the first method invocation in the sequence. This program provides a simple demonstration:

<!--p347-->
```java
//: exceptions/WhoCalled.java
// Programmatic access to stack trace information.
public class WhoCalled {
static void f() {
// Generate an exception to fill in the stack trace
try {
throw new Exception();
} catch (Exception e) {
for(StackTraceElement ste : e.getStackTrace())
System.out.println(ste.getMethodName());
}
}
static void g() { f(); }
static void h() { g(); }
public static void main(String[] args) {
f();
System.out.println("--------------------------------");
g();
System.out.println("--------------------------------");
h();
}
} /* Output:
f
main
--------------------------------
f
g
main
--------------------------------
f
g
h
main
*///:~
```
Here, we just print the method name, but you can also print the entire StackTraceElement, which contains additional information. Rethrowing an exception Sometimes you’ll want to rethrow the exception that you just caught, particularly when you use Exception to catch any exception. Since you already have the reference to the current exception, you can simply rethrow that reference:
```java
catch(Exception e) {
System.out.println("An exception was thrown");
throw e;
}
```
Rethrowing an exception causes it to go to the exception handlers in the nexthigher context. Any further catch clauses for the same try block are still ignored. In addition, everything about the exception object is preserved, so the handler at the higher context that catches the specific exception type can extract all the information from that object. If you simply rethrow the current exception, the information that you print about that exception in printStackTrace( ) will pertain to the exception’s origin, not the place where you rethrow it. If you want to install new stack trace information, you can do so by calling fillInStackTrace( ), which returns a Throwable object that it creates by stuffing the current stack information into the old exception object. Here’s what it looks like:
```java
//: exceptions/Rethrowing.java
// Demonstrating fillInStackTrace()
public class Rethrowing {
public static void f() throws Exception {
System.out.println("originating the exception in f()");
throw new Exception("thrown from f()");
}
public static void g() throws Exception {
try {
f();
} catch(Exception e) {
System.out.println("Inside g(),e.printStackTrace()");
e.printStackTrace(System.out);
throw e;
}
}
public static void h() throws Exception {
```

<!--p348-->
Error Handling with Exceptions
```java
try {
f();
} catch(Exception e) {
System.out.println("Inside h(),e.printStackTrace()");
e.printStackTrace(System.out);
throw (Exception)e.fillInStackTrace();
}
}
public static void main(String[] args) {
try {
g();
} catch(Exception e) {
System.out.println("main: printStackTrace()");
e.printStackTrace(System.out);
}
try {
h();
} catch(Exception e) {
System.out.println("main: printStackTrace()");
e.printStackTrace(System.out);
}
}
} /* Output:
originating the exception in f()
Inside g(),e.printStackTrace()
java.lang.Exception: thrown from f()
at Rethrowing.f(Rethrowing.java:7)
at Rethrowing.g(Rethrowing.java:11)
at Rethrowing.main(Rethrowing.java:29)
main: printStackTrace()
java.lang.Exception: thrown from f()
at Rethrowing.f(Rethrowing.java:7)
at Rethrowing.g(Rethrowing.java:11)
at Rethrowing.main(Rethrowing.java:29)
originating the exception in f()
Inside h(),e.printStackTrace()
java.lang.Exception: thrown from f()
at Rethrowing.f(Rethrowing.java:7)
at Rethrowing.h(Rethrowing.java:20)
at Rethrowing.main(Rethrowing.java:35)
main: printStackTrace()
java.lang.Exception: thrown from f()
at Rethrowing.h(Rethrowing.java:24)
at Rethrowing.main(Rethrowing.java:35)
*///:~
```
The line where fillInStackTrace( ) is called becomes the new point of origin of the exception. It’s also possible to rethrow a different exception from the one you caught. If you do this, you get a similar effect as when you use fillInStackTrace( )— the information about the original site of the exception is lost, and what you’re left with is the information pertaining to the new throw:

<!--p349-->
```java
//: exceptions/RethrowNew.java
// Rethrow a different object from the one that was caught.
class OneException extends Exception {
public OneException(String s) { super(s); }
}
class TwoException extends Exception {
public TwoException(String s) { super(s); }
}
public class RethrowNew {
public static void f() throws OneException {
System.out.println("originating the exception in f()");
throw new OneException("thrown from f()");
}
public static void main(String[] args) {
try {
try {
f();
} catch(OneException e) {
System.out.println(
"Caught in inner try, e.printStackTrace()");
e.printStackTrace(System.out);
throw new TwoException("from inner try");
}
} catch(TwoException e) {
System.out.println(
"Caught in outer try, e.printStackTrace()");
e.printStackTrace(System.out);
}
}
} /* Output:
originating the exception in f()
Caught in inner try, e.printStackTrace()
OneException: thrown from f()
at RethrowNew.f(RethrowNew.java:15)
at RethrowNew.main(RethrowNew.java:20)
Caught in outer try, e.printStackTrace()
TwoException: from inner try
at RethrowNew.main(RethrowNew.java:25)
*///:~
```
The final exception knows only that it came from the inner try block and not from f( ). You never have to worry about cleaning up the previous exception, or any exceptions for that matter. They’re all heap-based objects created with new, so the garbage collector automatically cleans them all up. Exception chaining Often you want to catch one exception and throw another, but still keep the information about the originating exception—this is called exception chaining. Prior to JDK 1.4, programmers had to write their own code to preserve the original exception information, but now all Throwable subclasses have the option to take a cause object in their constructor. The cause is intended to be the originating exception, and by passing it in you maintain the stack trace back to its origin, even though you’re creating and throwing a new exception. It’s interesting to note that the only Throwable subclasses that provide the cause argument in the constructor are the three fundamental exception classes Error (used by the JVM to report system errors), Exception, and RuntimeException. If you want to chain any other exception types, you do it through the initCause( ) method rather than the constructor. Here’s an example that allows you to dynamically add fields to a DynamicFields object at run time:
```java
//: exceptions/DynamicFields.java
```

<!--p350-->
Error Handling with Exceptions

<!--p351-->
```java
// A Class that dynamically adds fields to itself.
// Demonstrates exception chaining.
import static net.mindview.util.Print.*;
class DynamicFieldsException extends Exception {}
public class DynamicFields {
private Object[][] fields;
public DynamicFields(int initialSize) {
fields = new Object[initialSize][2];
for(int i = 0; i < initialSize; i++)
fields[i] = new Object[] { null, null };
}
public String toString() {
StringBuilder result = new StringBuilder();
for(Object[] obj : fields) {
result.append(obj[0]);
result.append(": ");
result.append(obj[1]);
result.append("\n");
}
return result.toString();
}
private int hasField(String id) {
for(int i = 0; i < fields.length; i++)
if(id.equals(fields[i][0]))
return i;
return -1;
}
private int
getFieldNumber(String id) throws NoSuchFieldException {
int fieldNum = hasField(id);
if(fieldNum == -1)
throw new NoSuchFieldException();
return fieldNum;
}
private int makeField(String id) {
for(int i = 0; i < fields.length; i++)
if(fields[i][0] == null) {
fields[i][0] = id;
return i;
}
// No empty fields. Add one:
Object[][] tmp = new Object[fields.length + 1][2];
for(int i = 0; i < fields.length; i++)
tmp[i] = fields[i];
for(int i = fields.length; i < tmp.length; i++)
tmp[i] = new Object[] { null, null };
fields = tmp;
// Recursive call with expanded fields:
return makeField(id);
}
public Object
getField(String id) throws NoSuchFieldException {
return fields[getFieldNumber(id)][1];
}
public Object setField(String id, Object value)
throws DynamicFieldsException {
if(value == null) {
// Most exceptions don’t have a "cause" constructor.
// In these cases you must use initCause(),
// available in all Throwable subclasses.
DynamicFieldsException dfe =
new DynamicFieldsException();
dfe.initCause(new NullPointerException());
throw dfe;
}
int fieldNumber = hasField(id);
if(fieldNumber == -1)
fieldNumber = makeField(id);
Object result = null;
try {
result = getField(id); // Get old value
} catch(NoSuchFieldException e) {
// Use constructor that takes "cause":
throw new RuntimeException(e);
}
fields[fieldNumber][1] = value;
return result;
}
public static void main(String[] args) {
DynamicFields df = new DynamicFields(3);
print(df);
try {
df.setField("d", "A value for d");
df.setField("number", 47);
df.setField("number2", 48);
print(df);
df.setField("d", "A new value for d");
df.setField("number3", 11);
print("df: " + df);
print("df.getField(\"d\") : " + df.getField("d"));
Object field = df.setField("d", null); // Exception
} catch(NoSuchFieldException e) {
e.printStackTrace(System.out);
} catch(DynamicFieldsException e) {
e.printStackTrace(System.out);
}
}
} /* Output:
null: null
null: null
null: null
d: A value for d
number: 47
number2: 48
df: d: A new value for d
number: 47
number2: 48
number3: 11
df.getField("d") : A new value for d
DynamicFieldsException
at DynamicFields.setField(DynamicFields.java:64)
at DynamicFields.main(DynamicFields.java:94)
Caused by: java.lang.NullPointerException
at DynamicFields.setField(DynamicFields.java:66)
... 1 more
*///:~
```

<!--p352-->
Each DynamicFields object contains an array of Object-Object pairs. The first object is the field identifier (a String), and the second is the field value, which can be any type except an unwrapped primitive. When you create the object, you make an educated guess about how many fields you need. When you call setField( ), it either finds the existing field by that Error Handling with Exceptions name or creates a new one, and puts in your value. If it runs out of space, it adds new space by creating an array of length one longer and copying the old elements in. If you try to put in a null value, then it throws a DynamicFieldsException by creating one and using initCause( ) to insert a NullPointerException as the cause. As a return value, setField( ) also fetches out the old value at that field location using getField( ), which could throw a NoSuchFieldException. If the client programmer calls getField( ), then they are responsible for handling NoSuchFieldException, but if this exception is thrown inside setField( ), it’s a programming error, so the NoSuchFieldException is converted to a RuntimeException using the constructor that takes a cause argument. You’ll notice that toString( ) uses a StringBuilder to create its result. You’ll learn more about StringBuilder in the Strings chapter, but in general you’ll want to use it whenever you’re writing a toString( ) that involves looping, as is the case here. Exercise 10:(2) Create a class with two methods, f( ) and g( ). In g( ), throw an exception of a new type that you define. In f( ), call g( ), catch its exception and, in the catch clause, throw a different exception (of a second type that you define). Test your code in main( ). Exercise 11:(1) Repeat the previous exercise, but inside the catch clause, wrap g( )’s exception in a RuntimeException. Standard Java exceptions The Java class Throwable describes anything that can be thrown as an exception. There are two general types of Throwable objects ("types of = "inherited from"). Error represents compile-time and system errors that you don’t worry about catching (except in very special cases). Exception is the basic type that can be thrown from any of the standard Java library class methods and from your methods and runtime accidents. So the Java programmer’s base type of interest is usually Exception. The best way to get an overview of the exceptions is to browse the JDK documentation. It’s worth doing this once just to get a feel for the various exceptions, but you’ll soon see that there isn’t anything special between one exception and the next except for the name. Also, the number of exceptions in Java keeps expanding; basically, it’s pointless to print them in a book. Any new library you get from a third-party vendor will probably have its own exceptions as well. The important thing to understand is the concept and what you should do with the exceptions. The basic idea is that the name of the exception represents the problem that occurred, and the exception name is intended to be relatively selfexplanatory. The exceptions are not all defined in java.lang;some are created to support other libraries such as util, net, and io, which you can see from their full class names or what they are inherited from. For example, all I/O exceptions are inherited from java.io.IOException.
## Special case: RuntimeException
The first example in this chapter was

<!--p353-->
```java
if(t == null)
throw new NullPointerException();
```
It can be a bit horrifying to think that you must check for null on every reference that is passed into a method (since you can’t know if the caller has passed you a valid reference). Fortunately, you don’t—this is part of the standard runtime checking that Java performs for you, and if any call is made to a null reference, Java will automatically throw a NullPointerException. So the above bit of code is always superfluous, although you may want to perform other checks in order to guard against the appearance of a NullPointerException. There’s a whole group of exception types that are in this category. They’re always thrown automatically by Java and you don’t need to include them in your exception specifications. Conveniently enough, they’re all grouped together by putting them under a single base class called RuntimeException, which is a perfect example of inheritance: It establishes a family of types that have some characteristics and behaviors in common. Also, you never need to write an exception specification saying that a method might throw a RuntimeException (or any type inherited from RuntimeException), because they are unchecked exceptions. Because they indicate bugs, you don’t usually catch a RuntimeException—it’s dealt with automatically. If you were forced to check for RuntimeExceptions, your code could get too messy. Even though you don’t typically catch RuntimeExceptions, in your own packages you might choose to throw some of the RuntimeExceptions. What happens when you don’t catch such exceptions? Since the compiler doesn’t enforce exception specifications for these, it’s quite plausible that a RuntimeException could percolate all the way out to your main( ) method without being caught. To see what happens in this case, try the following example:
```java
//: exceptions/NeverCaught.java
// Ignoring RuntimeExceptions.
// {ThrowsException}
public class NeverCaught {
static void f() {
throw new RuntimeException("From f()");
}
static void g() {
f();
}
public static void main(String[] args) {
g();
}
} ///:~
```
You can already see that a RuntimeException (or anything inherited from it) is a special case, since the compiler doesn’t require an exception specification for these types. The output is reported to System.err:
```java
Exception in thread "main" Java.lang.RuntimeException: From f()
at NeverCaught.f(NeverCaught.Java:7)
at NeverCaught.g(NeverCaught.Java:10)
at NeverCaught.main(NeverCaught.Java:13)
```

<!--p354-->
So the answer is: If a RuntimeException gets all the way out to main( ) without being caught, printStackTrace( ) is called for that exception as the program exits. Keep in mind that only exceptions of type RuntimeException (and subclasses) can be ignored in your coding, since the compiler carefully enforces the handling of all checked exceptions. The reasoning is that a RuntimeException represents a programming error, which is: Error Handling with Exceptions 1.An error you cannot anticipate. For example, a null reference that is outside of your control. 2. An error that you, as a programmer, should have checked for in your code (such as ArraylndexOutOfBoundsException where you should have paid attention to the size of the array). An exception that happens from point #1 often becomes an issue for point #2. You can see what a tremendous benefit it is to have exceptions in this case, since they help in the debugging process. It’s interesting to notice that you cannot classify Java exception handling as a single-purpose tool. Yes, it is designed to handle those pesky runtime errors that will occur because of forces outside your code’s control, but it’s also essential for certain types of programming bugs that the compiler cannot detect. Exercise 12:(3) Modify innerclasses/Sequence.java so that it throws an appropriate exception if you try to put in too many elements. Performing cleanup
## with finally
There’s often some piece of code that you want to execute whether or not an exception is thrown within a try block. This usually pertains to some operation other than memory recovery (since that’s taken care of by the garbage collector). To achieve this effect, you use a finally clause4 at the end of all the exception handlers. The full picture of an exception- handling section is thus:
```java
try {
// The guarded region: Dangerous activities
// that might throw A, B, or C
} catch(A a1) {
// Handler for situation A
} catch(B b1) {
// Handler for situation B
} catch(C c1) {
// Handler for situation C
} finally {
// Activities that happen every time
}
```
To demonstrate that the finally clause always runs, try this program:
```java
//: exceptions/FinallyWorks.java
// The finally clause is always executed.
class ThreeException extends Exception {}
public class FinallyWorks {
static int count = 0;
public static void main(String[] args) {
while(true) {
try {
```

<!--p355-->
4C++ exception handling does not have the finally clause because it relies on destructors to accomplish this sort of cleanup. Error Handling with Exceptions
```java
// Post-increment is zero first time:
if(count++ == 0)
throw new ThreeException();
System.out.println("No exception");
} catch(ThreeException e) {
System.out.println("ThreeException");
} finally {
System.out.println("In finally clause");
if(count == 2) break; // out of "while"
}
}
}
} /* Output:
ThreeException
In finally clause
No exception
In finally clause
*///:~
```
From the output, you can see that the finally clause is executed whether or not an exception is thrown. This program also gives a hint for how you can deal with the fact that exceptions in Java do not allow you to resume back to where the exception was thrown, as discussed earlier. If you place your try block in a loop, you can establish a condition that must be met before you continue the program. You can also add a static counter or some other device to allow the loop to try several different approaches before giving up. This way you can build a greater level of robustness into your programs.
## What’s finally for?
In a language without garbage collection and without automatic destructor calls,5finally is important because it allows the programmer to guarantee the release of memory regardless of what happens in the try block. But Java has garbage collection, so releasing memory is virtually never a problem. Also, it has no destructors to call. So when do you need to use finally in Java? The finally clause is necessary when you need to set something other than memory back to its original state. This is some kind of cleanup like an open file or network connection, something you’ve drawn on the screen, or even a switch in the outside world, as modeled in the following example:
```java
//: exceptions/Switch.java
import static net.mindview.util.Print.*;
public class Switch {
private boolean state = false;
public boolean read() { return state; }
public void on() { state = true; print(this); }
public void off() { state = false; print(this); }
public String toString() { return state ? "on" : "off"; }
} ///:~
//: exceptions/OnOffException1.java
public class OnOffException1 extends Exception {} ///:~
```

<!--p356-->
5A destructor is a function that’s always called when an object becomes unused. You always know exactly where and when the destructor gets called. C++ has automatic destructor calls, and C# (which is much more like Java) has a way that automatic destruction can occur.
```java
//: exceptions/OnOffException2.java
public class OnOffException2 extends Exception {} ///:~
//: exceptions/OnOffSwitch.java
// Why use finally?
public class OnOffSwitch {
private static Switch sw = new Switch();
public static void f()
throws OnOffException1,OnOffException2 {}
public static void main(String[] args) {
try {
sw.on();
// Code that can throw exceptions...
f();
sw.off();
} catch(OnOffException1 e) {
System.out.println("OnOffException1");
sw.off();
} catch(OnOffException2 e) {
System.out.println("OnOffException2");
sw.off();
}
}
} /* Output:
on
off
*///:~
```
The goal here is to make sure that the switch is off when main( ) is completed, so sw.off( ) is placed at the end of the try block and at the end of each exception handler. But it’s possible that an exception might be thrown that isn’t caught here, so sw.off( ) would be missed. However, with finally you can place the cleanup code from a try block in just one place:
```java
//: exceptions/WithFinally.java
// Finally Guarantees cleanup.
public class WithFinally {
static Switch sw = new Switch();
public static void main(String[] args) {
try {
sw.on();
// Code that can throw exceptions...
OnOffSwitch.f();
} catch(OnOffException1 e) {
System.out.println("OnOffException1");
} catch(OnOffException2 e) {
System.out.println("OnOffException2");
} finally {
sw.off();
}
}
} /* Output:
on
off
*///:~
```

<!--p357-->
Here the sw.off( ) has been moved to just one place, where it’s guaranteed to run no matter what happens. Even in cases in which the exception is not caught in the current set of catch clauses, finally will be executed before the exception-handling mechanism continues its search for a handler at the next higher level:
```java
//: exceptions/AlwaysFinally.java
// Finally is always executed.
import static net.mindview.util.Print.*;
class FourException extends Exception {}
public class AlwaysFinally {
public static void main(String[] args) {
print("Entering first try block");
try {
print("Entering second try block");
try {
throw new FourException();
} finally {
print("finally in 2nd try block");
}
} catch(FourException e) {
System.out.println(
"Caught FourException in 1st try block");
} finally {
System.out.println("finally in 1st try block");
}
}
} /* Output:
Entering first try block
Entering second try block
finally in 2nd try block
Caught FourException in 1st try block
finally in 1st try block
*///:~
```
The finally statement will also be executed in situations in which break and continue statements are involved. Note that, along with the labeled break and labeled continue, finally eliminates the need for a goto statement in Java. Exercise 13:(2) Modify Exercise 9 by adding a finally clause. Verify that your finally clause is executed, even if a NullPointerException is thrown. Exercise 14:(2) Show that OnOffSwitch.java can fail by throwing a RuntimeException inside the try block. Exercise 15:(2) Show that WithFinally.java doesn’t fail by throwing a RuntimeException inside the try block.
## Using finally during return
Because a finally clause is always executed, it’s possible to return from multiple points within a method and still guarantee that important cleanup will be performed:
```java
//: exceptions/MultipleReturns.java
import static net.mindview.util.Print.*;
public class MultipleReturns {
public static void f(int i) {
print("Initialization that requires cleanup");
```

<!--p358-->
Error Handling with Exceptions
```java
try {
print("Point 1");
if(i == 1) return;
print("Point 2");
if(i == 2) return;
print("Point 3");
if(i == 3) return;
print("End");
return;
} finally {
print("Performing cleanup");
}
}
public static void main(String[] args) {
for(int i = 1; i <= 4; i++)
f(i);
}
} /* Output:
Initialization that requires cleanup
Point 1
Performing cleanup
Initialization that requires cleanup
Point 1
Point 2
Performing cleanup
Initialization that requires cleanup
Point 1
Point 2
Point 3
Performing cleanup
Initialization that requires cleanup
Point 1
Point 2
Point 3
End
Performing cleanup
*///:~
```
You can see from the output that it doesn’t matter where you return from inside the finally class. Exercise 16:(2) Modify reusing/CADSystem.java to demonstrate that returning from the middle of a try-finally will still perform proper cleanup. Exercise 17:(3) Modify polymorphism/Frog.java so that it uses try-finally to guarantee proper cleanup, and show that this works even if you return from the middle of the try-finally. Pitfall: the lost exception Unfortunately, there’s a flaw in Java’s exception implementation. Although exceptions are an indication of a crisis in your program and should never be ignored, it’s possible for an exception to simply be lost. This happens with a particular configuration using a finally clause:

<!--p359-->
```java
//: exceptions/LostMessage.java
// How an exception can be lost.
class VeryImportantException extends Exception {
public String toString() {
return "A very important exception!";
}
}
class HoHumException extends Exception {
public String toString() {
return "A trivial exception";
}
}
public class LostMessage {
void f() throws VeryImportantException {
throw new VeryImportantException();
}
void dispose() throws HoHumException {
throw new HoHumException();
}
public static void main(String[] args) {
try {
LostMessage lm = new LostMessage();
try {
lm.f();
} finally {
lm.dispose();
}
} catch(Exception e) {
System.out.println(e);
}
}
} /* Output:
A trivial exception
*///:~
```
You can see from the output that there’s no evidence of the VerylmportantException, which is simply replaced by the HoHumException in the finally clause. This is a rather serious pitfall, since it means that an exception can be completely lost, and in a far more subtle and difficult-to-detect fashion than the preceding example. In contrast, C++ treats the situation in which a second exception is thrown before the first one is handled as a dire programming error. Perhaps a future version of Java will repair this problem (on the other hand, you will typically wrap any method that throws an exception, such as dispose( ) in the example above, inside a try-catch clause). An even simpler way to lose an exception is just to return from inside a finally clause:
```java
//: exceptions/ExceptionSilencer.java
public class ExceptionSilencer {
public static void main(String[] args) {
try {
throw new RuntimeException();
} finally {
// Using ‘return’ inside the finally block
// will silence any thrown exception.
return;
}
}
} ///:~
```

<!--p360-->
If you run this program you’ll see that it produces no output, even though an exception is thrown. Error Handling with Exceptions Exercise 18:(3) Add a second level of exception loss to LostMessage.java so that the HoHumException is itself replaced by a third exception. Exercise 19:(2) Repair the problem in LostMessage.java by guarding the call in the finally clause. Exception restrictions When you override a method, you can throw only the exceptions that have been specified in the base-class version of the method. This is a useful restriction, since it means that code that works with the base class will automatically work with any object derived from the base class (a fundamental OOP concept, of course), including exceptions. This example demonstrates the kinds of restrictions imposed (at compile time) for exceptions:

<!--p361-->
```java
//: exceptions/StormyInning.java
// Overridden methods may throw only the exceptions
// specified in their base-class versions, or exceptions
// derived from the base-class exceptions.
class BaseballException extends Exception {}
class Foul extends BaseballException {}
class Strike extends BaseballException {}
abstract class Inning {
public Inning() throws BaseballException {}
public void event() throws BaseballException {
// Doesn’t actually have to throw anything
}
public abstract void atBat() throws Strike, Foul;
public void walk() {} // Throws no checked exceptions
}
class StormException extends Exception {}
class RainedOut extends StormException {}
class PopFoul extends Foul {}
interface Storm {
public void event() throws RainedOut;
public void rainHard() throws RainedOut;
}
public class StormyInning extends Inning implements Storm {
// OK to add new exceptions for constructors, but you
// must deal with the base constructor exceptions:
public StormyInning()
throws RainedOut, BaseballException {}
public StormyInning(String s)
throws Foul, BaseballException {}
// Regular methods must conform to base class:
//! void walk() throws PopFoul {} //Compile error
// Interface CANNOT add exceptions to existing
// methods from the base class:
//! public void event() throws RainedOut {}
// If the method doesn’t already exist in the
// base class, the exception is OK:
public void rainHard() throws RainedOut {}
// You can choose to not throw any exceptions,
// even if the base version does:
public void event() {}
// Overridden methods can throw inherited exceptions:
public void atBat() throws PopFoul {}
public static void main(String[] args) {
try {
StormyInning si = new StormyInning();
si.atBat();
} catch(PopFoul e) {
System.out.println("Pop foul");
} catch(RainedOut e) {
System.out.println("Rained out");
} catch(BaseballException e) {
System.out.println("Generic baseball exception");
}
// Strike not thrown in derived version.
try {
// What happens if you upcast?
Inning i = new StormyInning();
i.atBat();
// You must catch the exceptions from the
// base-class version of the method:
} catch(Strike e) {
System.out.println("Strike");
} catch(Foul e) {
System.out.println("Foul");
} catch(RainedOut e) {
System.out.println("Rained out");
} catch(BaseballException e) {
System.out.println("Generic baseball exception");
}
}
} ///:~
```

<!--p362-->
In Inning, you can see that both the constructor and the event( ) method say that they will throw an exception, but they never do. This is legal because it allows you to force the user to catch any exceptions that might be added in overridden versions of event( ). The same idea holds for abstract methods, as seen in atBat( ). The interface Storm is interesting because it contains one method (event( )) that is defined in Inning, and one method that isn’t. Both methods throw a new type of exception, RainedOut. When Stormylnning extends Inning and implements Storm, you’ll see that the event( ) method in Storm cannot change the exception interface of event( ) in Inning. Again, this makes sense because otherwise you’d never know if you were catching the correct thing when working with the base class. Of course, if a method described in an interface is not in the base class, such as rainHard( ), then there’s no problem if it throws exceptions. The restriction on exceptions does not apply to constructors. You can see in Stormylnning that a constructor can throw anything it wants, regardless of what the base-class constructor throws. However, since a base-class constructor must always be called one way or another (here, the default constructor is called automatically), the derived-class constructor must declare any base-class constructor exceptions in its exception specification. A derived-class constructor cannot catch exceptions thrown by its base-class constructor. The reason StormyInning.walk( ) will not compile is that it throws an exception, but Inning.walk( ) does not. If this were allowed, then you could write code that called Inning.walk( ) and that didn’t have to handle any exceptions, but then when you substituted an object of a class derived from Inning, exceptions would be thrown so your Error Handling with Exceptions code would break. By forcing the derived-class methods to conform to the exception specifications of the base-class methods, substitutability of objects is maintained. The overridden event( ) method shows that a derived-class version of a method may choose not to throw any exceptions, even if the base-class version does. Again, this is fine since it doesn’t break code that is written assuming the base-class version throws exceptions. Similar logic applies to atBat( ), which throws PopFoul, an exception that is derived from Foul thrown by the base-class version of atBat( ). This way, if you write code that works with Inning and calls atBat( ), you must catch the Foul exception. Since PopFoul is derived from Foul, the exception handler will also catch PopFoul. The last point of interest is in main( ). Here, you can see that if you’re dealing with exactly a StormyInning object, the compiler forces you to catch only the exceptions that are specific to that class, but if you upcast to the base type, then the compiler (correctly) forces you to catch the exceptions for the base type. All these constraints produce much more robust exceptionhandling code.6 Although exception specifications are enforced by the compiler during inheritance, the exception specifications are not part of the type of a method, which comprises only the method name and argument types. Therefore, you cannot overload methods based on exception specifications. In addition, just because an exception specification exists in a base- class version of a method doesn’t mean that it must exist in the derived-class version of the method. This is quite different from inheritance rules, where a method in the base class must also exist in the derived class. Put another way, the "exception specification interface" for a particular method may narrow during inheritance and overriding, but it may not widen—this is precisely the opposite of the rule for the class interface during inheritance. Exercise 20:(3) Modify StormyInning.java by adding an UmpireArgument exception type and methods that throw this exception. Test the modified hierarchy. Constructors It’s important that you always ask, "If an exception occurs, will everything be properly cleaned up?" Most of the time you’re fairly safe, but with constructors there’s a problem. The constructor puts the object into a safe starting state, but it might perform some operation— such as opening a filethat doesn’t get cleaned up until the user is finished with the object and calls a special cleanup method. If you throw an exception from inside a constructor, these cleanup behaviors might not occur properly. This means that you must be especially diligent while you write your constructor. You might think that finally is the solution. But it’s not quite that simple, because finally performs the cleanup code every time. If a constructor fails partway through its execution, it might not have successfully created some part of the object that will be cleaned up in the finally clause. In the following example, a class called InputFile is created that opens a file and allows you to read it one line at a time. It uses the classes FileReader and BufferedReader from the Java standard I/O library that will be discussed in the I/O chapter. These classes are simple enough that you probably won’t have any trouble understanding their basic use:
```java
//: exceptions/InputFile.java
// Paying attention to exceptions in constructors.
import java.io.*;
```

<!--p363-->
6ISO C++ added similar constraints that require derived-method exceptions to be the same as, or derived from, the exceptions thrown by the base-class method. This is one case in which C++ is actually able to check exception specifications at compile time.
```java
public class InputFile {
private BufferedReader in;
public InputFile(String fname) throws Exception {
try {
in = new BufferedReader(new FileReader(fname));
// Other code that might throw exceptions
} catch(FileNotFoundException e) {
System.out.println("Could not open " + fname);
// Wasn’t open, so don’t close it
throw e;
} catch(Exception e) {
// All other exceptions must close it
try {
in.close();
} catch(IOException e2) {
System.out.println("in.close() unsuccessful");
}
throw e; // Rethrow
} finally {
// Don’t close it here!!!
}
}
public String getLine() {
String s;
try {
s = in.readLine();
} catch(IOException e) {
throw new RuntimeException("readLine() failed");
}
return s;
}
public void dispose() {
try {
in.close();
System.out.println("dispose() successful");
} catch(IOException e2) {
throw new RuntimeException("in.close() failed");
}
}
} ///:~
```

<!--p364-->
The constructor for InputFile takes a String argument, which is the name of the file you want to open. Inside a try block, it creates a FileReader using the file name. A FileReader isn’t particularly useful until you use it to create a BufferedReader. One of the benefits of InputFile is that it combines these two actions. If the FileReader constructor is unsuccessful, it throws a FileNotFoundException. This is the one case in which you don’t want to close the file, because it wasn’t successfully opened. Any other catch clauses must close the file because it was opened by the time those catch clauses are entered. (Of course, this gets trickier if more than one method can throw a FileNotFoundException. In that case, you’ll usually have to break things into several try blocks.) The close( ) method might throw an exception so it is tried and caught even though it’s within the block of another catch clause—it’s just another pair of curly braces to the Java compiler. After performing local operations, the exception is rethrown, which is appropriate because this constructor failed, and you don’t want the calling method to assume that the object has been properly created and is valid. In this example, the finally clause is definitely not the place to close( ) the file, since that would close it every time the constructor completed. We want the file to be open for the useful lifetime of the InputFile object. Error Handling with Exceptions The getLine( ) method returns a String containing the next line in the file. It calls readLine( ), which can throw an exception, but that exception is caught so that getLine( ) doesn’t throw any exceptions. One of the design issues with exceptions is whether to handle an exception completely at this level, to handle it partially and pass the same exception (or a different one) on, or whether to simply pass it on. Passing it on, when appropriate, can certainly simplify coding. In this situation, the getLine( ) method converts the exception to a RuntimeException to indicate a programming error. The dispose( ) method must be called by the user when the InputFile object is no longer needed. This will release the system resources (such as file handles) that are used by the BufferedReader and/or FileReader objects. You don’t want to do this until you’re finished with the InputFile object. You might think of putting such functionality into a finalize( ) method, but as mentioned in the Initialization & Cleanup chapter, you can’t always be sure that finalize( ) will be called (even if you can be sure that it will be called, you don’t know when). This is one of the downsides to Java: All cleanupother than memory cleanup—doesn’t happen automatically, so you must inform the client programmers that they are responsible. The safest way to use a class which might throw an exception during construction and which requires cleanup is to use nested try blocks:
```java
//: exceptions/Cleanup.java
// Guaranteeing proper cleanup of a resource.
public class Cleanup {
public static void main(String[] args) {
try {
InputFile in = new InputFile("Cleanup.java");
try {
String s;
int i = 1;
while((s = in.getLine()) != null)
; // Perform line-by-line processing here...
} catch(Exception e) {
System.out.println("Caught Exception in main");
e.printStackTrace(System.out);
} finally {
in.dispose();
}
} catch(Exception e) {
System.out.println("InputFile construction failed");
}
}
} /* Output:
dispose() successful
*///:~
```
Look carefully at the logic here: The construction of the InputFile object is effectively in its own try block. If that construction fails, the outer catch clause is entered and dispose( ) is not called. However, if construction succeeds then you want to make sure the object is cleaned up, so immediately after construction you create a new try block. The finally that performs cleanup is associated with the inner try block; this way, the finally clause is not executed if construction fails, and it is always executed if construction succeeds. This general cleanup idiom should still be used if the constructor throws no exceptions. The basic rule is: Right after you create an object that requires cleanup, begin a try-finally:

<!--p365-->
```java
//: exceptions/CleanupIdiom.java
// Each disposable object must be followed by a try-finally
class NeedsCleanup { // Construction can’t fail
private static long counter = 1;
private final long id = counter++;
public void dispose() {
System.out.println("NeedsCleanup " + id + " disposed");
}
}
class ConstructionException extends Exception {}
class NeedsCleanup2 extends NeedsCleanup {
// Construction can fail:
public NeedsCleanup2() throws ConstructionException {}
}
public class CleanupIdiom {
public static void main(String[] args) {
// Section 1:
NeedsCleanup nc1 = new NeedsCleanup();
try {
// ...
} finally {
nc1.dispose();
}
// Section 2:
// If construction cannot fail you can group objects:
NeedsCleanup nc2 = new NeedsCleanup();
NeedsCleanup nc3 = new NeedsCleanup();
try {
// ...
} finally {
nc3.dispose(); // Reverse order of construction
nc2.dispose();
}
// Section 3:
// If construction can fail you must guard each one:
try {
NeedsCleanup2 nc4 = new NeedsCleanup2();
try {
NeedsCleanup2 nc5 = new NeedsCleanup2();
try {
// ...
} finally {
nc5.dispose();
}
} catch(ConstructionException e) { // nc5 constructor
System.out.println(e);
} finally {
nc4.dispose();
}
} catch(ConstructionException e) { // nc4 constructor
System.out.println(e);
}
}
} /* Output:
NeedsCleanup 1 disposed
NeedsCleanup 3 disposed
NeedsCleanup 2 disposed
NeedsCleanup 5 disposed
NeedsCleanup 4 disposed
*///:~
```

<!--p366-->
Error Handling with Exceptions In main( ), section 1 is fairly straightforward: You follow a disposable object with a try- finally. If the object construction cannot fail, no catch is necessary. In section 2, you can see that objects with constructors that cannot fail can be grouped together for both construction and cleanup. Section 3 shows how to deal with objects whose constructors can fail and which need cleanup. To properly handle this situation, things get messy, because you must surround each construction with its own try-catch, and each object construction must be followed by a try-finally to guarantee cleanup. The messiness of exception handling in this case is a strong argument for creating constructors that cannot fail, although this is not always possible. Note that if dispose( ) can throw an exception you might need additional try blocks. Basically, you must think carefully about all the possibilities and guard for each one. Exercise 21:(2) Demonstrate that a derived-class constructor cannot catch exceptions thrown by its base-class constructor. Exercise 22:(2) Create a class called FailingConstructor with a constructor that might fail partway through the construction process and throw an exception. In main( ), write code that properly guards against this failure. Exercise 23:(4) Add a class with a dispose( ) method to the previous exercise. Modify FailingConstructor so that the constructor creates one of these disposable objects as a member object, after which the constructor might throw an exception, after which it creates a second disposable member object. Write code to properly guard against failure, and in main( ) verify that all possible failure situations are covered. Exercise 24: (3)Add a dispose( ) method to the FailingConstructor class and write code to properly use this class. Exception matching When an exception is thrown, the exception-handling system looks through the "nearest" handlers in the order they are written. When it finds a match, the exception is considered handled, and no further searching occurs. Matching an exception doesn’t require a perfect match between the exception and its handler. A derived-class object will match a handler for the base class, as shown in this example:

<!--p367-->
```java
//: exceptions/Human.java
// Catching exception hierarchies.
class Annoyance extends Exception {}
class Sneeze extends Annoyance {}
public class Human {
public static void main(String[] args) {
// Catch the exact type:
try {
throw new Sneeze();
} catch(Sneeze s) {
System.out.println("Caught Sneeze");
} catch(Annoyance a) {
System.out.println("Caught Annoyance");
}
// Catch the base type:
try {
throw new Sneeze();
} catch(Annoyance a) {
System.out.println("Caught Annoyance");
}
}
} /* Output:
Caught Sneeze
Caught Annoyance
*///:~
```
The Sneeze exception will be caught by the first catch clause that it matches, which is the first one, of course. However, if you remove the first catch clause, leaving only the catch clause for Annoyance, the code still works because it’s catching the base class of Sneeze. Put another way, catch(Annoyance a) will catch an Annoyance or any class derived from it. This is useful because if you decide to add more derived exceptions to a method, then the client programmer’s code will not need changing as long as the client catches the base- class exceptions. If you try to "mask" the derived-class exceptions by putting the base-class catch clause first, like this:
```java
try {
throw new Sneeze();
} catch(Annoyance a) {
// ...
} catch(Sneeze s) {
// ...
}
```

<!--p368-->
the compiler will give you an error message, since it sees that the Sneeze catch clause can never be reached. Exercise 25:(2) Create a three-level hierarchy of exceptions. Now create a base-class A with a method that throws an exception at the base of your hierarchy. Inherit B from A and override the method so it throws an exception at level two of your hierarchy. Repeat by inheriting class C from B. In main( ), create a C and upcast it to A, then call the method. Alternative approaches An exception-handling system is a trapdoor that allows your program to abandon execution of the normal sequence of statements. The trapdoor is used when an "exceptional condition" occurs, such that normal execution is no longer possible or desirable. Exceptions represent conditions that the current method is unable to handle. The reason exception-handling systems were developed is because the approach of dealing with each possible error condition produced by each function call was too onerous, and programmers simply weren’t doing it. As a result, they were ignoring the errors. It’s worth observing that the issue of programmer convenience in handling errors was a prime motivation for exceptions in the first place. One of the important guidelines in exception handling is "Don’t catch an exception unless you know what to do with it." In fact, one of the important goals of exception handling is to move the error-handling code away from the point where the errors occur. This allows you to focus on what you want to accomplish in one section of your code, and how you’re going to deal with problems in a distinct separate section of your code. As a result, your mainline code is not cluttered with error-handling logic, and it’s much easier to understand and maintain. Error Handling with Exceptions Exception handling also tends to reduce the amount of error-handling code, by allowing one handler to deal with many error sites. Checked exceptions complicate this scenario a bit, because they force you to add catch clauses in places where you may not be ready to handle an error. This results in the "harmful if swallowed" problem:
```java
try {
// ... to do something useful
} catch(ObligatoryException e) {} // Gulp!
```

<!--p369-->

<!--p370-->

<!--p371-->
Programmers (myself included, in the 1st edition of this book) would just do the simplest thing, and "swallow" the exception—often unintentionally, but once you do it, the compiler has been satisfied, so unless you remember to revisit and correct the code, the exception will be lost. The exception happens, but it vanishes completely when swallowed. Because the compiler forces you to write code right away to handle the exception, this seems like the easiest solution even though it’s probably the worst thing you can do. Horrified upon realizing that I had done this, in the 2ndedition I "fixed" the problem by printing the stack trace inside the handler (as is still seen— appropriately—in a number of examples in this chapter). While this is useful to trace the behavior of exceptions, it still indicates that you don’t really know what to do with the exception at that point in your code. In this section you’ll learn about some of the issues and complications arising from checked exceptions, and options that you have when dealing with them. This topic seems simple. But it is not only complicated, it is also an issue of some volatility. There are people who are staunchly rooted on either side of the fence and who feel that the correct answer (theirs) is blatantly obvious. I believe the reason for one of these positions is the distinct benefit seen in going from a poorly typed language like pre-ANSI C to a strong, statically typed language (that is, checked at compile time) like C++ or Java. When you make that transition (as I did), the benefits are so dramatic that it can seem like static type checking is always the best answer to most problems. My hope is to relate a little bit of my own evolution that has brought the absolute value of static type checking into question; clearly, it’s very helpful much of the time, but there’s a fuzzy line we cross when it begins to get in the way and become a hindrance (one of my favorite quotes is "All models are wrong. Some are useful."). History Exception handling originated in systems like PL/1 and Mesa, and later appeared in CLU, Smalltalk, Modula-3, Ada, Eiffel, C++, Python, Java, and the post-Java languages Ruby and C#. The Java design is similar to C++, except in places where the Java designers felt that the C++ approach caused problems. To provide programmers with a framework that they were more likely to use for error handling and recovery, exception handling was added to C++ rather late in the standardization process, promoted by Bjarne Stroustrup, the language’s original author. The model for C++ exceptions came primarily from CLU. However, other languages existed at that time that also supported exception handling: Ada, Smalltalk (both of these had exceptions but no exception specifications) and Modula-3 (which included both exceptions and specifications). In their seminal paper7 on the subject, Liskov and Snyder observe that a major defect of languages like C, which report errors in a transient fashion, is that: 7Barbara Liskov and Alan Snyder, Exception Handling in CLU, IEEE Transactions on Software Engineering, Vol. SE-5, No. 6, November 1979. This paper is not available on the Internet, only in print form, so you’ll have to contact a library to get a copy. "...every invocation must be followed by a conditional test to determine what the outcome was. This requirement leads to programs that are difficult to read, and probably inefficient as well, thus discouraging programmers from signaling and handling exceptions." Thus one of the original motivations of exception handling was to prevent this requirement, but with checked exceptions in Java we commonly see exactly this kind of code. They go on to say: "...requiring that the text of a handler be attached to the invocation that raises the exception would lead to unreadable programs in which expressions were broken up with handlers." Following the CLU approach when designing C++ exceptions, Stroustrup stated that the goal was to reduce the amount of code required to recover from errors. I believe that he was observing that programmers were typically not writing error-handling code in C because the amount and placement of such code was daunting and distracting. As a result, they were used to doing it the C way, ignoring errors in code and using debuggers to track down problems. To use exceptions, these C programmers had to be convinced to write "additional" code that they weren’t normally writing. Thus, to draw them into a better way of handling errors, the amount of code they would need to "add" must not be onerous. I think it’s important to keep this goal in mind when looking at the effects of checked exceptions in Java. C++ brought an additional idea over from CLU: the exception specification, to programmatically state in the method signature the exceptions that could result from calling that method. The exception specification really has two purposes. It can say, "I’m originating this exception in my code; you handle it." But it can also mean, "I’m ignoring this exception that can occur as a result of my code; you handle it." We’ve been focusing on the "you handle it" part when looking at the mechanics and syntax of exceptions, but here I’m particularly interested in the fact that we often ignore exceptions and that’s what the exception specification can state. In C++ the exception specification is not part of the type information of a function. The only compile-time checking is to ensure that exception specifications are used consistently; for example, if a function or method throws exceptions, then the overloaded or derived versions must also throw those exceptions. Unlike Java, however, no compile-time checking occurs to determine whether or not the function or method will actually throw that exception, or whether the exception specification is complete (that is, whether it accurately describes all exceptions that maybe thrown). That validation does happen, but only at run time. If an exception is thrown that violates the exception specification, the C++ program will call the standard library function unexpected( ). It is interesting to note that, because of the use of templates, exception specifications are not used at all in the Standard C++ Library. In Java, there are restrictions on the way that Java generics can be used with exception specifications. Perspectives First, it’s worth noting that Java effectively invented the checked exception (clearly inspired by C++ exception specifications and the fact that C++ programmers typically don’t bother with them). However, it was an experiment which no subsequent language has chosen to duplicate. Secondly, checked exceptions appear to be an "obvious good thing" when seen in introductory examples and in small programs. It has been suggested that the subtle difficulties begin to appear when programs start to get large. Of course, largeness usually doesn’t happen overnight; it creeps. Languages that may not be suited for large-scale projects Error Handling with Exceptions are used for small projects. These projects grow, and at some point we realize that things have gone from "manageable" to "difficult." This is what I’m suggesting may be the case with too much type checking; in particular, with checked exceptions. The scale of the program seems to be a significant issue. This is a problem because most discussions tend to use small programs as demonstrations. One of the C# designers observed that: "Examination of small programs leads to the conclusion that requiring exception specifications could both enhance developer productivity and enhance code quality, but experience with large software projects suggests a different result—decreased productivity and little or no increase in code quality."8 In reference to uncaught exceptions, the CLU creators stated: "We felt it was unrealistic to require the programmer to provide handlers in situations where no meaningful action can be taken."9 When explaining why a function declaration with no specification means that it can throw any exception, rather than no exceptions, Stroustrup states: "However, that would require exception specifications for essentially every function, would be a significant cause for recompilation, and would inhibit cooperation with software written in other languages. This would encourage programmers to subvert the exception-handling mechanisms and to write spurious code to suppress exceptions. It would provide a false sense of security to people who failed to notice the exception."10 We see this very behavior—subverting the exceptions—happening with checked exceptions in Java. Martin Fowler (author of UML Distilled, Refactoring, and Analysis Patterns) wrote the following to me: "...on the whole I think that exceptions are good, but Java checked exceptions are more trouble than they are worth." I now think that Java’s important step was to unify the error-reporting model, so that all errors are reported using exceptions. This wasn’t happening with C++, because for backward compatibility with C the old model of just ignoring errors was still available. But if you have consistent reporting with exceptions, then exceptions can be used if desired, and if not, they will propagate out to the highest level (the console or other container program). When Java modified the C++ model so that exceptions were the only way to report errors, the extra enforcement of checked exceptions may have become less necessary. In the past, I have been a strong believer that both checked exceptions and static type checking were essential to robust program development. However, both anecdotal and direct experience11with languages that are more dynamic than static has led me to think that the great benefits actually come from: 8http://discuss.develop.com/archives/wa.exe?A2=indoonA&L=DOTNET&P=R32820 9 Exception Handling in CLU, Liskov & Snyder. 10 Bjarne Stroustrup, The C++ Programming Language, 3rd Edition (Addison-Wesley, 1997), P- 376. 11 Indirectly with Smalltalk via conversations with many experienced programmers in that language; directly with Python (www.Python.org). Error Handling with Exceptions 1.A unified error-reporting model via exceptions, regardless of whether the programmer is forced by the compiler to handle them. 2.Type checking, regardless of when it takes place. That is, as long as proper use of a type is enforced, it often doesn’t matter if it happens at compile time or run time. On top of this, there are very significant productivity benefits to reducing the compile-time constraints upon the programmer. Indeed, reflection and generics are required to compensate for the overconstraining nature of static typing, as you shall see in a number of examples throughout the book. I’ve already been told by some that what I say here constitutes blasphemy, and by uttering these words my reputation will be destroyed, civilizations will fall, and a higher percentage of programming projects will fail. The belief that the compiler can save your project by pointing out errors at compile time runs strong, but it’s even more important to realize the limitation of what the compiler is able to do; in the supplement you will find at http://MindView.net/Books/BetterJava, I emphasize the value of an automated build process and unit testing, which give you far more leverage than you get by trying to turn everything into a syntax error. It’s worth keeping in mind that: "A good programming language is one that helps programmers write good programs. No programming language will prevent its users from writing bad programs."12 In any event, the likelihood of checked exceptions ever being removed from Java seems dim. It would be too radical of a language change, and proponents within Sun appear to be quite strong. Sun has a history and policy of absolute backwards compatibility—to give you a sense of this, virtually all Sun software runs on all Sun hardware, no matter how old. However, if you find that some checked exceptions are getting in your way, or especially if you find yourself being forced to catch exceptions, but you don’t know what to do with them, there are some alternatives. Passing exceptions to the console In simple programs, like many of those in this book, the easiest way to preserve the exceptions without writing a lot of code is to pass them out of main( ) to the console. For example, if you want to open a file for reading (something you’ll learn about in detail in the I/O chapter), you must open and close a FilelnputStream, which throws exceptions. For a simple program, you can do this (you’ll see this approach used in numerous places throughout this book):
```java
//: exceptions/MainException.java
import java.io.*;
public class MainException {
// Pass all exceptions to the console:
public static void main(String[] args) throws Exception {
// Open the file:
FileInputStream file =
new FileInputStream("MainException.java");
// Use the file ...
// Close the file:
file.close();
}
} ///:~
```

<!--p372-->
12Kees Koster, designer of the CDL language, as quoted by Bertrand Meyer, designer of the Eiffel language, www.elj.com/elj/vi/ni/bm/right/. Note that main( ) is also a method that may have an exception specification, and here the type of exception is Exception, the root class of all checked exceptions. By passing it out to the console, you are relieved from writing try-catch clauses within the body of main( ). (Unfortunately, file I/O is significantly more complex than it would appear to be from this example, so don’t get too excited until after you’ve read the I/O chapter). Exercise 26:(1) Change the file name string in MainException.java to name a file that doesn’t exist. Run the program and note the result. Converting checked to unchecked exceptions Throwing an exception from main( ) is convenient when you’re writing simple programs for your own consumption, but is not generally useful. The real problem is when you are writing an ordinary method body, and you call another method and realize, "I have no idea what to do with this exception here, but I don’t want to swallow it or print some banal message." With chained exceptions, a new and simple solution prevents itself. You simply "wrap" a checked exception inside a RuntimeException by passing it to the RuntimeException constructor, like this: t r y {
```java
// ... to do something useful
} catch(IDontKnowWhatToDoWithThisCheckedException e) {
throw new RuntimeException(e);
}
```
This seems to be an ideal solution if you want to "turn off the checked exception—you don’t swallow it, and you don’t have to put it in your method’s exception specification, but because of exception chaining you don’t lose any information from the original exception. This technique provides the option to ignore the exception and let it bubble up the call stack without being required to write try-catch clauses and/or exception specifications. However, you may still catch and handle the specific exception by using getCause( ), as seen here:

<!--p373-->
```java
//: exceptions/TurnOffChecking.java
// "Turning off" Checked exceptions.
import java.io.*;
import static net.mindview.util.Print.*;
class WrapCheckedException {
void throwRuntimeException(int type) {
try {
switch(type) {
case 0: throw new FileNotFoundException();
case 1: throw new IOException();
case 2: throw new RuntimeException("Where am I?");
default: return;
}
} catch(Exception e) { // Adapt to unchecked:
throw new RuntimeException(e);
}
}
}
class SomeOtherException extends Exception {}
public class TurnOffChecking {
public static void main(String[] args) {
WrapCheckedException wce = new WrapCheckedException();
// You can call throwRuntimeException() without a try
// block, and let RuntimeExceptions leave the method:
wce.throwRuntimeException(3);
// Or you can choose to catch exceptions:
for(int i = 0; i < 4; i++)
try {
if(i < 3)
wce.throwRuntimeException(i);
else
throw new SomeOtherException();
} catch(SomeOtherException e) {
print("SomeOtherException: " + e);
} catch(RuntimeException re) {
try {
throw re.getCause();
} catch(FileNotFoundException e) {
print("FileNotFoundException: " + e);
} catch(IOException e) {
print("IOException: " + e);
} catch(Throwable e) {
print("Throwable: " + e);
}
}
}
} /* Output:
FileNotFoundException: java.io.FileNotFoundException
IOException: java.io.IOException
Throwable: java.lang.RuntimeException: Where am I?
SomeOtherException: SomeOtherException
*///:~
```

<!--p374-->

<!--p375-->
WrapCheckedException.throwRuntimeException( ) contains code that generates different types of exceptions. These are caught and wrapped inside RuntimeException objects, so they become the "cause" of those exceptions. In TurnOffChecking, you can see that it’s possible to call throwRuntimeException( ) with no try block because the method does not throw any checked exceptions. However, when you’re ready to catch exceptions, you still have the ability to catch any exception you want by putting your code inside a try block. You start by catching all the exceptions you explicitly know might emerge from the code in your try block—in this case, SomeOtherException is caught first. Lastly, you catch RuntimeException and throw the result of getCause( ) (the wrapped exception). This extracts the originating exceptions, which can then be handled in their own catch clauses. The technique of wrapping a checked exception in a RuntimeException will be used when appropriate throughout the rest of this book. Another solution is to create your own subclass of RuntimeException. This way, it doesn’t need to be caught, but someone can catch it if they want to. Exercise 27:(1) Modify Exercise 3 to convert the exception to a RuntimeException. Exercise 28:(1) Modify Exercise 4 so that the custom exception class inherits from RuntimeException, and show that the compiler allows you to leave out the try block. Exercise 29:(1) Modify all the exception types in Stormylnning.java so that they extend RuntimeException, and show that no exception specifications or try blocks are necessary. Remove the ‘//!’ comments and show how the methods can be compiled without specifications. Error Handling with Exceptions Exercise 30: (2) Modify Human.java so that the exceptions inherit from RuntimeException. Modify main( ) so that the technique in TurnOffChecking.java is used to handle the different types of exceptions. Exception guidelines Use exceptions to: 1.Handle problems at the appropriate level. (Avoid catching exceptions unless you know what to do with them.) 2.Fix the problem and call the method that caused the exception again. 3.Patch things up and continue without retrying the method. 4.Calculate some alternative result instead of what the method was supposed to produce. 5.Do whatever you can in the current context and rethrow the same exception to a higher context. 6.Do whatever you can in the current context and throw a different exception to a higher context. 7.Terminate the program. 8.Simplify. (If your exception scheme makes things more complicated, then it is painful and annoying to use.) 9.Make your library and program safer. (This is a short-term investment for debugging, and a long-term investment for application robustness.) Summary Exceptions are integral to programming with Java; you can accomplish only so much without knowing how to work with them. For that reason, exceptions are introduced at this point in the book—there are many libraries (like I/O, mentioned earlier) that you can’t use without handling exceptions. One of the advantages of exception handling is that it allows you to concentrate on the problem you’re trying to solve in one place, and then deal with the errors from that code in another place. And although exceptions are generally explained as tools that allow you to report and recover from errors at run time, I have come to wonder how often the "recovery" aspect is implemented, or even possible. My perception is that it is less than 10 percent of the time, and even then it probably amounts to unwinding the stack to a known stable state rather than actually performing any kind of resumptive behavior. Whether or not this is true, I have come to believe that the "reporting" function is where the essential value of exceptions lie. The fact that Java effectively insists that all errors be reported in the form of exceptions is what gives it a great advantage over languages like C++, which allow you to report errors in a number of different ways, or not at all. A consistent error- reporting system means that you no longer have to ask the question "Are errors slipping through the cracks?" with each piece of code you write (as long as you don’t "swallow" the exceptions, that is!). Error Handling with Exceptions As you will see in future chapters, by laying this question to rest—even if you do so by throwing a RuntimeException—your design and implementation efforts can be focused on more interesting and challenging issues. Solutions to selected exercises can be found in the electronic document The Thinking in Java Annotated Solution Guide, available for sale from www.MindView.net.