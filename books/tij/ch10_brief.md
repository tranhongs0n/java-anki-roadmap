# 10. Inner Classes (printed p243-274)


<!--p265-->
Inner Classes It’s possible to place a class definition within another class definition. This is called an inner class. The inner class is a valuable feature because it allows you to group classes that logically belong together and to control the visibility of one within the other. However, it’s important to understand that inner classes are distinctly different from composition. At first, inner classes look like a simple code-hiding mechanism: You place classes inside other classes. You’ll learn, however, that the inner class does more than that—it knows about and can communicate with the surrounding class—and the kind of code you can write with inner classes is more elegant and clear, although there’s certainly no guarantee of this. Initially, inner classes may seem odd, and it will take some time to become comfortable using them in your designs. The need for inner classes isn’t always obvious, but after the basic syntax and semantics of inner classes have been described, the section "Why inner classes?" should begin to make clear the benefits of inner classes. After that section, the remainder of the chapter contains more detailed explorations of the syntax of inner classes. These features are provided for language completeness, but you might not need to use them, at least not at first. So the initial parts of the chapter might be all you need for now, and you can leave the more detailed explorations as reference material. Creating inner classes You create an inner class just as you’d expect—by placing the class definition inside a surrounding class:

<!--p266-->
```java
//: innerclasses/Parcel1.java
// Creating inner classes.
public class Parcel1 {
class Contents {
private int i = 11;
public int value() { return i; }
}
class Destination {
private String label;
Destination(String whereTo) {
label = whereTo;
}
String readLabel() { return label; }
}
// Using inner classes looks just like
// using any other class, within Parcel1:
public void ship(String dest) {
Contents c = new Contents();
Destination d = new Destination(dest);
System.out.println(d.readLabel());
}
public static void main(String[] args) {
Parcel1 p = new Parcel1();
p.ship("Tasmania");
}
} /* Output:
Tasmania
*///:~
```
The inner classes used inside ship( ) look just like ordinary classes. Here, the only practical difference is that the names are nested within Parceli. You’ll see in a while that this isn’t the only difference. More typically, an outer class will have a method that returns a reference to an inner class, as you can see in the to( ) and contents( ) methods:
```java
//: innerclasses/Parcel2.java
// Returning a reference to an inner class.
public class Parcel2 {
class Contents {
private int i = 11;
public int value() { return i; }
}
class Destination {
private String label;
Destination(String whereTo) {
label = whereTo;
}
String readLabel() { return label; }
}
public Destination to(String s) {
return new Destination(s);
}
public Contents contents() {
return new Contents();
}
public void ship(String dest) {
Contents c = contents();
Destination d = to(dest);
System.out.println(d.readLabel());
}
public static void main(String[] args) {
Parcel2 p = new Parcel2();
p.ship("Tasmania");
Parcel2 q = new Parcel2();
// Defining references to inner classes:
Parcel2.Contents c = q.contents();
Parcel2.Destination d = q.to("Borneo");
}
} /* Output:
Tasmania
*///:~
```

<!--p267-->
If you want to make an object of the inner class anywhere except from within a non-static method of the outer class, you must specify the type of that object as OuterClassName.InnerClassName, as seen in main( ). Exercise 1: (1) Write a class named Outer that contains an inner class named Inner. Add a method to Outer that returns an object of type Inner. In main( ), create and initialize a reference to an Inner. The link to the outer class So far, it appears that inner classes are just a name-hiding and code organization scheme, which is helpful but not totally compelling. However, there’s another twist. When you create Inner Classes an inner class, an object of that inner class has a link to the enclosing object that made it, and so it can access the members of that enclosing object—without any special qualifications. In addition, inner classes have access rights to all the elements in the enclosing class.1The following example demonstrates this:
```java
//: innerclasses/Sequence.java
// Holds a sequence of Objects.
interface Selector {
boolean end();
Object current();
void next();
}
public class Sequence {
private Object[] items;
private int next = 0;
public Sequence(int size) { items = new Object[size]; }
public void add(Object x) {
if(next < items.length)
items[next++] = x;
}
private class SequenceSelector implements Selector {
private int i = 0;
public boolean end() { return i == items.length; }
public Object current() { return items[i]; }
public void next() { if(i < items.length) i++; }
}
public Selector selector() {
return new SequenceSelector();
}
public static void main(String[] args) {
Sequence sequence = new Sequence(10);
for(int i = 0; i < 10; i++)
sequence.add(Integer.toString(i));
Selector selector = sequence.selector();
while(!selector.end()) {
System.out.print(selector.current() + " ");
selector.next();
}
}
} /* Output:
0 1 2 3 4 5 6 7 8 9
*///:~
```

<!--p268-->
The Sequence is simply a fixed-sized array of Object with a class wrapped around it. You call add( ) to add a new Object to the end of the sequence (if there’s room left). To fetch each of the objects in a Sequence, there’s an interface called Selector. This is an example of the Iterator design pattern that you shall learn more about later in the book. A Selector allows you to see if you’re at the end( ), to access the current( ) Object, and to move to the next( ) Object in the Sequence. Because Selector is an interface, other classes can implement the interface in their own ways, and other methods can take the interface as an argument, in order to create more general-purpose code. Here, the SequenceSelector is a private class that provides Selector functionality. In main( ), you can see the creation of a Sequence, followed by the addition of a number of String objects. Then, a Selector is produced with a call to selector( ), and this is used to move through the Sequence and select each item. 1This is very different from the design of nested classes in C++, which is simply a namehiding mechanism. There is no link to an enclosing object and no implied permissions in C++. At first, the creation of SequenceSelector looks like just another inner class. But examine it closely. Note that each of the methods—end( ), current( ), and next( )—refers to items, which is a reference that isn’t part of SequenceSelector, but is instead a private field in the enclosing class. However, the inner class can access methods and fields from the enclosing class as if it owned them. This turns out to be very convenient, as you can see in the preceding example. So an inner class has automatic access to the members of the enclosing class. How can this happen? The inner class secretly captures a reference to the particular object of the enclosing class that was responsible for creating it. Then, when you refer to a member of the enclosing class, that reference is used to select that member. Fortunately, the compiler takes care of all these details for you, but now you can see that an object of an inner class can be created only in association with an object of the enclosing class (when, as you shall see, the inner class is non-static). Construction of the inner-class object requires the reference to the object of the enclosing class, and the compiler will complain if it cannot access that reference. Most of the time this occurs without any intervention on the part of the programmer. Exercise 2:(1) Create a class that holds a String, and has a toString( ) method that displays this String. Add several instances of your new class to a Sequence object, then display them. Exercise 3:(1) Modify Exercise 1 so that Outer has a private String field (initialized by the constructor), and Inner has a toString( ) that displays this field. Create an object of type Inner and display it.
## Using .this and .new
If you need to produce the reference to the outer-class object, you name the outer class followed by a dot and this. The resulting reference is automatically the correct type, which is known and checked at compile time, so there is no runtime overhead. Here’s an example that shows how to use .this:
```java
//: innerclasses/DotThis.java
// Qualifying access to the outer-class object.
public class DotThis {
void f() { System.out.println("DotThis.f()"); }
public class Inner {
public DotThis outer() {
return DotThis.this;
// A plain "this" would be Inner’s "this"
}
}
public Inner inner() { return new Inner(); }
public static void main(String[] args) {
DotThis dt = new DotThis();
DotThis.Inner dti = dt.inner();
dti.outer().f();
}
} /* Output:
DotThis.f()
*///:~
```
Sometimes you want to tell some other object to create an object of one of its inner classes. To do this you must provide a reference to the other outer-class object in the new expression, using the .new syntax, like this:

<!--p269-->
```java
//: innerclasses/DotNew.java
// Creating an inner class directly using the .new syntax.
public class DotNew {
public class Inner {}
public static void main(String[] args) {
DotNew dn = new DotNew();
DotNew.Inner dni = dn.new Inner();
}
} ///:~
```
To create an object of the inner class directly, you don’t follow the same form and refer to the outer class name DotNew as you might expect, but instead you must use an object of the outer class to make an object of the inner class, as you can see above. This also resolves the name scoping issues for the inner class, so you don’t say (indeed, you can’t say) dn.new DotNew.Inner( ). It’s not possible to create an object of the inner class unless you already have an object of the outer class. This is because the object of the inner class is quietly connected to the object of the outer class that it was made from. However, if you make a nested class (a static inner class), then it doesn’t need a reference to the outer-class object. Here, you see the use of .new applied to the "Parcel" example:
```java
//: innerclasses/Parcel3.java
// Using .new to create instances of inner classes.
public class Parcel3 {
class Contents {
private int i = 11;
public int value() { return i; }
}
class Destination {
private String label;
Destination(String whereTo) { label = whereTo; }
String readLabel() { return label; }
}
public static void main(String[] args) {
Parcel3 p = new Parcel3();
// Must use instance of outer class
// to create an instance of the inner class:
Parcel3.Contents c = p.new Contents();
Parcel3.Destination d = p.new Destination("Tasmania");
}
} ///:~
```

<!--p270-->
Exercise 4:(2) Add a method to the class Sequence.SequenceSelector that produces the reference to the outer class Sequence. Exercise 5:(1) Create a class with an inner class. In a separate class, make an instance of the inner class. Inner classes and upcasting Inner classes really come into their own when you start upcasting to a base class, and in particular to an interface. (The effect of producing an interface reference from an object that implements it is essentially the same as upcasting to a base class.) That’s because the inner class—the implementation of the interface—can then be unseen and unavailable, which is Inner Classes convenient for hiding the implementation. All you get back is a reference to the base class or the interface. We can create interfaces for the previous examples:
```java
//: innerclasses/Destination.java
public interface Destination {
String readLabel();
} ///:~
```
Now Contents and Destination represent interfaces available to the client programmer. Remember that an interface automatically makes all of its members public. When you get a reference to the base class or the interface, it’s possible that you can’t even find out the exact type, as shown here:
```java
//: innerclasses/TestParcel.java
class Parcel4 {
private class PContents implements Contents {
private int i = 11;
public int value() { return i; }
}
protected class PDestination implements Destination {
private String label;
private PDestination(String whereTo) {
label = whereTo;
}
public String readLabel() { return label; }
}
public Destination destination(String s) {
return new PDestination(s);
}
public Contents contents() {
return new PContents();
}
}
public class TestParcel {
public static void main(String[] args) {
Parcel4 p = new Parcel4();
Contents c = p.contents();
Destination d = p.destination("Tasmania");
// Illegal -- can’t access private class:
//! Parcel4.PContents pc = p.new PContents();
}
} ///:~
```

<!--p271-->
In Parcel4, something new has been added: The inner class PContents is private, so nothing but Parcel4 can access it. Normal (non-inner) classes cannot be made private or protected;they may only be given public or package access. PDestination is protected, so nothing but Parcel4, classes in the same package (since protected also gives package access), and the inheritors of Parcel4 can access PDestination. This means that the client programmer has restricted knowledge and access to these members. In fact, you can’t even downcast to a private inner class (or a protected inner class unless you’re an inheritor), because you can’t access the name, as you can see in class TestParcel. Thus, the private inner class provides a way for the class designer to completely prevent any type-coding dependencies and to completely hide details about implementation. In addition, extension of an interface is useless from the client programmer’s perspective since the client programmer cannot access any additional methods that aren’t part of the public interface. This also provides an opportunity for the Java compiler to generate more efficient code. Exercise 6:(2) Create an interface with at least one method, in its own package. Create a class in a separate package. Add a protected inner class that implements the interface. In a third package, inherit from your class and, inside a method, return an object of the protected inner class, upcasting to the interface during the return. Exercise 7:(2) Create a class with a private field and a private method. Create an inner class with a method that modifies the outer-class field and calls the outer-class method. In a second outer-class method, create an object of the inner class and call its method, then show the effect on the outer-class object. Exercise 8:(2) Determine whether an outer class has access to the private elements of its inner class. Inner classes in methods and scopes What you’ve seen so far encompasses the typical use for inner classes. In general, the code that you’ll write and read involving inner classes will be "plain" inner classes that are simple and easy to understand. However, the syntax for inner classes covers a number of other, more obscure techniques. Inner classes can be created within a method or even an arbitrary scope. There are two reasons for doing this: 1.As shown previously, you’re implementing an interface of some kind so that you can create and return a reference. 2.You’re solving a complicated problem and you want to create a class to aid in your solution, but you don’t want it publicly available. In the following examples, the previous code will be modified to use: 1.A class defined within a method 2.A class defined within a scope inside a method 3.An anonymous class implementing an interface 4.An anonymous class extending a class that has a non-default constructor 5.An anonymous class that performs field initialization 6.An anonymous class that performs construction using instance initialization (anonymous inner classes cannot have constructors) The first example shows the creation of an entire class within the scope of a method (instead of the scope of another class). This is called a local inner class:
```java
//: innerclasses/Parcel5.java
// Nesting a class within a method.
public class Parcel5 {
public Destination destination(String s) {
class PDestination implements Destination {
```

<!--p272-->
Inner Classes
```java
private String label;
private PDestination(String whereTo) {
label = whereTo;
}
public String readLabel() { return label; }
}
return new PDestination(s);
}
public static void main(String[] args) {
Parcel5 p = new Parcel5();
Destination d = p.destination("Tasmania");
}
} ///:~
```
The class PDestination is part of destination( ) rather than being part of Parcels. Therefore, PDestination cannot be accessed outside of destination( ). Notice the upcasting that occurs in the return statementnothing comes out of destination( ) except a reference to Destination, the base class. Of course, the fact that the name of the class PDestinationis placed inside destination( ) doesn’t mean that PDestination is not a valid object once destination( ) returns. You could use the class identifier PDestination for an inner class inside each class in the same subdirectory without a name clash. The next example shows how you can nest an inner class within any arbitrary scope:
```java
//: innerclasses/Parcel6.java
// Nesting a class within a scope.
public class Parcel6 {
private void internalTracking(boolean b) {
if(b) {
class TrackingSlip {
private String id;
TrackingSlip(String s) {
id = s;
}
String getSlip() { return id; }
}
TrackingSlip ts = new TrackingSlip("slip");
String s = ts.getSlip();
}
// Can’t use it here! Out of scope:
//! TrackingSlip ts = new TrackingSlip("x");
}
public void track() { internalTracking(true); }
public static void main(String[] args) {
Parcel6 p = new Parcel6();
p.track();
}
} ///:~
```

<!--p273-->
The class TrackingSlip is nested inside the scope of an if statement. This does not mean that the class is conditionally created—it gets compiled along with everything else. However, it’s not available outside the scope in which it is defined. Other than that, it looks just like an ordinary class. Exercise 9:(1) Create an interface with at least one method, and implement that interface by defining an inner class within a method, which returns a reference to your interface. Exercise 10:(1) Repeat the previous exercise but define the inner class within a scope within a method. Exercise 11:(2) Create a private inner class that implements a public interface. Write a method that returns a reference to an instance of the private inner class, upcast to the interface. Show that the inner class is completely hidden by trying to downcast to it. Anonymous inner classes The next example looks a little odd:
```java
//: innerclasses/Parcel7.java
// Returning an instance of an anonymous inner class.
public class Parcel7 {
public Contents contents() {
return new Contents() { // Insert a class definition
private int i = 11;
public int value() { return i; }
}; // Semicolon required in this case
}
public static void main(String[] args) {
Parcel7 p = new Parcel7();
Contents c = p.contents();
}
} ///:~
```
The contents( ) method combines the creation of the return value with the definition of the class that represents that return value! In addition, the class is anonymous; it has no name. To make matters a bit worse, it looks like you’re starting out to create a Contents object, But then, before you get to the semicolon, you say, "But wait, I think I’ll slip in a class definition." What this strange syntax means is "Create an object of an anonymous class that’s inherited from Contents."The reference returned by the new expression is automatically upcast to a Contents reference. The anonymous inner-class syntax is a shorthand for:
```java
//: innerclasses/Parcel7b.java
// Expanded version of Parcel7.java
public class Parcel7b {
class MyContents implements Contents {
private int i = 11;
public int value() { return i; }
}
public Contents contents() { return new MyContents(); }
public static void main(String[] args) {
Parcel7b p = new Parcel7b();
Contents c = p.contents();
}
} ///:~
```
In the anonymous inner class, Contents is created by using a default constructor. The following code shows what to do if your base class needs a constructor with an argument:
```java
//: innerclasses/Parcel8.java
// Calling the base-class constructor.
```

<!--p274-->
Inner Classes
```java
public class Parcel8 {
public Wrapping wrapping(int x) {
// Base constructor call:
return new Wrapping(x) { // Pass constructor argument.
public int value() {
return super.value() * 47;
}
}; // Semicolon required
}
public static void main(String[] args) {
Parcel8 p = new Parcel8();
Wrapping w = p.wrapping(10);
}
} ///:~
```
That is, you simply pass the appropriate argument to the base-class constructor, seen here as the x passed in new Wrapping(x). Although it’s an ordinary class with an implementation, Wrapping is also being used as a common "interface" to its derived classes:
```java
//: innerclasses/Wrapping.java
public class Wrapping {
private int i;
public Wrapping(int x) { i = x; }
public int value() { return i; }
} ///:~
```
You’ll notice that Wrapping has a constructor that requires an argument, to make things a bit more interesting. The semicolon at the end of the anonymous inner class doesn’t mark the end of the class body. Instead, it marks the end of the expression that happens to contain the anonymous class. Thus, it’s identical to the use of the semicolon everywhere else. You can also perform initialization when you define fields in an anonymous class:
```java
//: innerclasses/Parcel9.java
// An anonymous inner class that performs
// initialization. A briefer version of Parcel5.java.
public class Parcel9 {
// Argument must be final to use inside
// anonymous inner class:
public Destination destination(final String dest) {
return new Destination() {
private String label = dest;
public String readLabel() { return label; }
};
}
public static void main(String[] args) {
Parcel9 p = new Parcel9();
Destination d = p.destination("Tasmania");
}
} ///:~
```

<!--p275-->
If you’re defining an anonymous inner class and want to use an object that’s defined outside the anonymous inner class, the compiler requires that the argument reference be final, as you see in the argument to destination( ). If you forget, you’ll get a compile-time error message. As long as you’re simply assigning a field, the approach in this example is fine. But what if you need to perform some constructor-like activity? You can’t have a named constructor in an anonymous class (since there’s no name!), but with instance initialization, you can, in effect, create a constructor for an anonymous inner class, like this:
```java
//: innerclasses/AnonymousConstructor.java
// Creating a constructor for an anonymous inner class.
import static net.mindview.util.Print.*;
abstract class Base {
public Base(int i) {
print("Base constructor, i = " + i);
}
public abstract void f();
}
public class AnonymousConstructor {
public static Base getBase(int i) {
return new Base(i) {
{ print("Inside instance initializer"); }
public void f() {
print("In anonymous f()");
}
};
}
public static void main(String[] args) {
Base base = getBase(47);
base.f();
}
} /* Output:
Base constructor, i = 47
Inside instance initializer
In anonymous f()
*///:~
```
In this case, the variable i did nor have to be final. While i is passed to the base constructor of the anonymous class, it is never directly used inside the anonymous class. Here’s the "parcel" theme with instance initialization. Note that the arguments to destination( ) must be final since they are used within the anonymous class:
```java
//: innerclasses/Parcel10.java
// Using "instance initialization" to perform
// construction on an anonymous inner class.
public class Parcel10 {
public Destination
destination(final String dest, final float price) {
return new Destination() {
private int cost;
// Instance initialization for each object:
{
cost = Math.round(price);
if(cost > 100)
System.out.println("Over budget!");
}
private String label = dest;
public String readLabel() { return label; }
};
}
public static void main(String[] args) {
Parcel10 p = new Parcel10();
```

<!--p276-->
Inner Classes
```java
Destination d = p.destination("Tasmania", 101.395F);
}
} /* Output:
Over budget!
*///:~
```
Inside the instance initializer you can see code that couldn’t be executed as part of a field initializer (that is, the if statement). So in effect, an instance initializer is the constructor for an anonymous inner class. Of course, it’s limited; you can’t overload instance initializers, so you can have only one of these constructors. Anonymous inner classes are somewhat limited compared to regular inheritance, because they can either extend a class or implement an interface, but not both. And if you do implement an interface, you can only implement one. Exercise 12:(1) Repeat Exercise 7 using an anonymous inner class. Exercise 13:(1) Repeat Exercise 9 using an anonymous inner class. Exercise 14:(1) Modify interfaces/HorrorShow.java to implement DangerousMonster and Vampire using anonymous classes. Exercise 15:(2) Create a class with a non-default constructor (one with arguments) and no default constructor (no "no-arg" constructor). Create a second class that has a method that returns a reference to an object of the first class. Create the object that you return by making an anonymous inner class that inherits from the first class. Factory Method revisited Look at how much nicer the interfaces/Factories.java example comes out when you use anonymous inner classes:

<!--p277-->
```java
//: innerclasses/Factories.java
import static net.mindview.util.Print.*;
interface Service {
void method1();
void method2();
}
interface ServiceFactory {
Service getService();
}
class Implementation1 implements Service {
private Implementation1() {}
public void method1() {print("Implementation1 method1");}
public void method2() {print("Implementation1 method2");}
public static ServiceFactory factory =
new ServiceFactory() {
public Service getService() {
return new Implementation1();
}
};
}
class Implementation2 implements Service {
private Implementation2() {}
public void method1() {print("Implementation2 method1");}
public void method2() {print("Implementation2 method2");}
public static ServiceFactory factory =
new ServiceFactory() {
public Service getService() {
return new Implementation2();
}
};
}
public class Factories {
public static void serviceConsumer(ServiceFactory fact) {
Service s = fact.getService();
s.method1();
s.method2();
}
public static void main(String[] args) {
serviceConsumer(Implementation1.factory);
// Implementations are completely interchangeable:
serviceConsumer(Implementation2.factory);
}
} /* Output:
Implementation1 method1
Implementation1 method2
Implementation2 method1
Implementation2 method2
*///:~
```
Now the constructors for Implementation1 and Implementation2 can be private, and there’s no need to create a named class as the factory. In addition, you often only need a single factory object, and so here it has been created as a static field in the Service implementation. The resulting syntax is more meaningful, as well. The interfaces/Games.java example can also be improved with anonymous inner classes:
```java
//: innerclasses/Games.java
// Using anonymous inner classes with the Game framework.
import static net.mindview.util.Print.*;
interface Game { boolean move(); }
interface GameFactory { Game getGame(); }
class Checkers implements Game {
private Checkers() {}
private int moves = 0;
private static final int MOVES = 3;
public boolean move() {
print("Checkers move " + moves);
return ++moves != MOVES;
}
public static GameFactory factory = new GameFactory() {
public Game getGame() { return new Checkers(); }
};
}
class Chess implements Game {
private Chess() {}
private int moves = 0;
private static final int MOVES = 4;
public boolean move() {
print("Chess move " + moves);
return ++moves != MOVES;
```

<!--p278-->
Inner Classes
```java
}
public static GameFactory factory = new GameFactory() {
public Game getGame() { return new Chess(); }
};
}
public class Games {
public static void playGame(GameFactory factory) {
Game s = factory.getGame();
while(s.move())
;
}
public static void main(String[] args) {
playGame(Checkers.factory);
playGame(Chess.factory);
}
} /* Output:
Checkers move 0
Checkers move 1
Checkers move 2
Chess move 0
Chess move 1
Chess move 2
Chess move 3
*///:~
```
Remember the advice given at the end of the last chapter: Prefer classes to interfaces. If your design demands an interface, you’ll know it. Otherwise, don’t put it in until you are forced to. Exercise 16:(1) Modify the solution to Exercise 18 from the Interfaces chapter to use anonymous inner classes. Exercise 17:(1) Modify the solution to Exercise 19 from the Interfaces chapter to use anonymous inner classes. Nested classes If you don’t need a connection between the inner-class object and the outerclass object, then you can make the inner class static. This is commonly called a nested class.2To understand the meaning of static when applied to inner classes, you must remember that the object of an ordinary inner class implicitly keeps a reference to the object of the enclosing class that created it. This is not true, however, when you say an inner class is static. A nested class means: 1.You don’t need an outer-class object in order to create an object of a nested class. 2.You can’t access a non-static outer-class object from an object of a nested class. Nested classes are different from ordinary inner classes in another way, as well. Fields and methods in ordinary inner classes can only be at the outer level of a class, so ordinary inner classes cannot have static data, static fields, or nested classes. However, nested classes can have all of these:
```java
//: innerclasses/Parcel11.java
// Nested classes (static inner classes).
```

<!--p279-->
2Roughly similar to nested classes in C++, except that those classes cannot access private members as they can in Java.
```java
public class Parcel11 {
private static class ParcelContents implements Contents {
private int i = 11;
public int value() { return i; }
}
protected static class ParcelDestination
implements Destination {
private String label;
private ParcelDestination(String whereTo) {
label = whereTo;
}
public String readLabel() { return label; }
// Nested classes can contain other static elements:
public static void f() {}
static int x = 10;
static class AnotherLevel {
public static void f() {}
static int x = 10;
}
}
public static Destination destination(String s) {
return new ParcelDestination(s);
}
public static Contents contents() {
return new ParcelContents();
}
public static void main(String[] args) {
Contents c = contents();
Destination d = destination("Tasmania");
}
} ///:~
```
In main( ), no object of Parcel11 is necessary; instead, you use the normal syntax for selecting a static member to call the methods that return references to Contents and Destination. As you’ve seen earlier in this chapter, in an ordinary (non-static)inner class, the link to the outer-class object is achieved with a special this reference. A nested class does not have a special this reference, which makes it analogous to a static method. Exercise 18:(1) Create a class containing a nested class. In main( ), create an instance of the nested class. Exercise 19:(2) Create a class containing an inner class that itself contains an inner class. Repeat this using nested classes. Note the names of the .class files produced by the compiler. Classes inside interfaces Normally, you can’t put any code inside an interface, but a nested class can be part of an interface. Any class you put inside an interface is automatically public and static. Since the class is static, it doesn’t violate the rules for interfaces—the nested class is only placed inside the namespace of the interface. You can even implement the surrounding interface in the inner class, like this:
```java
//: innerclasses/ClassInInterface.java
// {main: ClassInInterface$Test}
```

<!--p280-->
Inner Classes
```java
public interface ClassInInterface {
void howdy();
class Test implements ClassInInterface {
public void howdy() {
System.out.println("Howdy!");
}
public static void main(String[] args) {
new Test().howdy();
}
}
} /* Output:
Howdy!
*///:~
```
It’s convenient to nest a class inside an interface when you want to create some common code to be used with all different implementations of that interface. Earlier in this book I suggested putting a main( ) in every class to act as a test bed for that class. One drawback to this is the amount of extra compiled code you must carry around. If this is a problem, you can use a nested class to hold your test code:
```java
//: innerclasses/TestBed.java
// Putting test code in a nested class.
// {main: TestBed$Tester}
public class TestBed {
public void f() { System.out.println("f()"); }
public static class Tester {
public static void main(String[] args) {
TestBed t = new TestBed();
t.f();
}
}
} /* Output:
f()
*///:~
```

<!--p281-->
This generates a separate class called TestBed$Tester (to run the program, you say Java TestBed$Tester, but you must escape the ‘$’ under Unix/Linux systems). You can use this class for testing, but you don’t need to include it in your shipping product; you can simply delete TestBed$Tester.class before packaging things up. Exercise 20:(1) Create an interface containing a nested class. Implement this interface and create an instance of the nested class. Exercise 21:(2) Create an interface that contains a nested class that has a static method that calls the methods of your interface and displays the results. Implement your interface and pass an instance of your implementation to the method. Inner Classes Reaching outward from a multiply nested class It doesn’t matter how deeply an inner class may be nested—it can transparently access all of the members of all the classes it is nested within, as seen here:3
```java
//: innerclasses/MultiNestingAccess.java
// Nested classes can access all members of all
// levels of the classes they are nested within.
class MNA {
private void f() {}
class A {
private void g() {}
public class B {
void h() {
g();
f();
}
}
}
}
public class MultiNestingAccess {
public static void main(String[] args) {
MNA mna = new MNA();
MNA.A mnaa = mna.new A();
MNA.A.B mnaab = mnaa.new B();
mnaab.h();
}
} ///:~
```

<!--p282-->
You can see that in MNAAB, the methods g( ) and f( ) are callable without any qualification (despite the fact that they are private). This example also demonstrates the syntax necessary to create objects of multiply nested inner classes when you create the objects in a different class. The ".new" syntax produces the correct scope, so you do not have to qualify the class name in the constructor call. Why inner classes? At this point you’ve seen a lot of syntax and semantics describing the way inner classes work, but this doesn’t answer the question of why they exist. Why did the Java designers go to so much trouble to add this fundamental language feature? Typically, the inner class inherits from a class or implements an interface, and the code in the inner class manipulates the outer-class object that it was created within. So you could say that an inner class provides a kind of window into the outer class. A question that cuts to the heart of inner classes is this: If I just need a reference to an interface, why don’t I just make the outer class implement that interface? The answer is "If that’s all you need, then that’s how you should do it." So what is it that distinguishes an inner class implementing an interface from an outer class implementing the same interface? The answer is that you can’t always have the convenience of interfaces—sometimes you’re working with implementations. So the most compelling reason for inner classes is: 3Thanks again to Martin Danner. Each inner class can independently inherit from an implementation. Thus, the inner class is not limited by whether the outer class is already inheriting from an implementation. Without the ability that inner classes provide to inherit—in effect—from more than one concrete or abstract class, some design and programming problems would be intractable. So one way to look at the inner class is as the rest of the solution of the multiple-inheritance problem. Interfaces solve part of the problem, but inner classes effectively allow "multiple implementation inheritance." That is, inner classes effectively allow you to inherit from more than one non-interface. To see this in more detail, consider a situation in which you have two interfaces that must somehow be implemented within a class. Because of the flexibility of interfaces, you have two choices: a single class or an inner class.
```java
//: innerclasses/MultiInterfaces.java
// Two ways that a class can implement multiple interfaces.
package innerclasses;
interface A {}
interface B {}
class X implements A, B {}
class Y implements A {
B makeB() {
// Anonymous inner class:
return new B() {};
}
}
public class MultiInterfaces {
static void takesA(A a) {}
static void takesB(B b) {}
public static void main(String[] args) {
X x = new X();
Y y = new Y();
takesA(x);
takesA(y);
takesB(x);
takesB(y.makeB());
}
} ///:~
```
Of course, this assumes that the structure of your code makes logical sense either way. However, you’ll ordinarily have some kind of guidance from the nature of the problem about whether to use a single class or an inner class. But without any other constraints, the approach in the preceding example doesn’t really make much difference from an implementation standpoint. Both of them work. However, if you have abstract or concrete classes instead of interfaces, you are suddenly limited to using inner classes if your class must somehow implement both of the others:

<!--p283-->
```java
//: innerclasses/MultiImplementation.java
// With concrete or abstract classes, inner
// classes are the only way to produce the effect
// of "multiple implementation inheritance."
package innerclasses;
class D {}
abstract class E {}
class Z extends D {
E makeE() { return new E() {}; }
}
public class MultiImplementation {
static void takesD(D d) {}
static void takesE(E e) {}
public static void main(String[] args) {
Z z = new Z();
takesD(z);
takesE(z.makeE());
}
} ///:~
```

<!--p284-->
If you didn’t need to solve the "multiple implementation inheritance" problem, you could conceivably code around everything else without the need for inner classes. But with inner classes you have these additional features: 1.The inner class can have multiple instances, each with its own state information that is independent of the information in the outer-class object. 2.In a single outer class you can have several inner classes, each of which implements the same interface or inherits from the same class in a different way. An example of this will be shown shortly. 3.The point of creation of the inner-class object is not tied to the creation of the outer- class object. 4.There is no potentially confusing "is-a" relationship with the inner class; it’s a separate entity. As an example, if Sequence.java did not use inner classes, you’d have to say, "A Sequence is a Selector,"and you’d only be able to have one Selector in existence for a particular Sequence. You can easily have a second method, reverseSelector( ), that produces a Selector that moves backward through the sequence. This kind of flexibility is only available with inner classes. Exercise 22:(2) Implement reverseSelector( ) in Sequence.java. Exercise 23:(4) Create an interface U with three methods. Create a class A with a method that produces a reference to a U by building an anonymous inner class. Create a second class B that contains an array of U. B should have one method that accepts and stores a reference to a U in the array, a second method that sets a reference in the array (specified by the method argument) to null, and a third method that moves through the array and calls the methods in U. In main( ), create a group of A objects and a single B. Fill the B with U references produced by the A objects. Use the B to call back into all the A objects. Remove some of the U references from the B. Closures & callbacks A closure is a callable object that retains information from the scope in which it was created. From this definition, you can see that an inner class is an object-oriented closure, because it doesn’t just contain each piece of information from the outer-class object ("the scope in which it was created"), but it automatically holds a reference back to the whole outer-class object, where it has permission to manipulate all the members, even private ones. Inner Classes One of the most compelling arguments made to include some kind of pointer mechanism in Java was to allow callbacks. With a callback, some other object is given a piece of information that allows it to call back into the originating object at some later point. This is a very powerful concept, as you will see later in the book. If a callback is implemented using a pointer, however, you must rely on the programmer to behave properly and not misuse the pointer. As you’ve seen by now, Java tends to be more careful than that, so pointers were not included in the language. The closure provided by the inner class is a good solution—more flexible and far safer than a pointer. Here’s an example:

<!--p285-->
```java
//: innerclasses/Callbacks.java
// Using inner classes for callbacks
package innerclasses;
import static net.mindview.util.Print.*;
interface Incrementable {
void increment();
}
// Very simple to just implement the interface:
class Callee1 implements Incrementable {
private int i = 0;
public void increment() {
i++;
print(i);
}
}
class MyIncrement {
public void increment() { print("Other operation"); }
static void f(MyIncrement mi) { mi.increment(); }
}
// If your class must implement increment() in
// some other way, you must use an inner class:
class Callee2 extends MyIncrement {
private int i = 0;
public void increment() {
super.increment();
i++;
print(i);
}
private class Closure implements Incrementable {
public void increment() {
// Specify outer-class method, otherwise
// you’d get an infinite recursion:
Callee2.this.increment();
}
}
Incrementable getCallbackReference() {
return new Closure();
}
}
class Caller {
private Incrementable callbackReference;
Caller(Incrementable cbh) { callbackReference = cbh; }
void go() { callbackReference.increment(); }
}
public class Callbacks {
public static void main(String[] args) {
Callee1 c1 = new Callee1();
Callee2 c2 = new Callee2();
MyIncrement.f(c2);
Caller caller1 = new Caller(c1);
Caller caller2 = new Caller(c2.getCallbackReference());
caller1.go();
caller1.go();
caller2.go();
caller2.go();
}
} /* Output:
Other operation
Other operation
Other operation
*///:~
```

<!--p286-->
This also shows a further distinction between implementing an interface in an outer class versus doing so in an inner class. Callee1 is clearly the simpler solution in terms of the code. Callee2 inherits from Mylncrement, which already has a different increment( ) method that does something unrelated to the one expected by the Incrementable interface. When Mylncrement is inherited into Callee2, increment( ) can’t be overridden for use by Incrementable, so you’re forced to provide a separate implementation using an inner class. Also note that when you create an inner class, you do not add to or modify the interface of the outer class. Everything except getCallbackReference( ) in Callee2 is private. To allow any connection to the outside world, the interface Incrementable is essential. Here you can see how interfaces allow for a complete separation of interface from implementation. The inner class Closure implements Incrementableto provide a hook back into Callee2— but a safe hook. Whoever gets the Incrementable reference can, of course, only call increment( ) and has no other abilities (unlike a pointer, which would allow you to run wild). Caller takes an Incrementable reference in its constructor (although the capturing of the callback reference could happen at any time) and then, sometime later, uses the reference to "call back" into the Callee class. The value of the callback is in its flexibility; you can dynamically decide what methods will be called at run time. The benefit of this will become more evident in the Graphical User Interfaces chapter, where callbacks are used everywhere to implement GUI functionality. Inner classes & control frameworks A more concrete example of the use of inner classes can be found in something that I will refer to here as a control framework. An application framework is a class or a set of classes that’s designed to solve a particular type of problem. To apply an application framework, you typically inherit from one or more classes and override some of the methods. The code that you write in the overridden methods customizes the general solution provided by that application framework in order to solve your specific problem. This is an example of the Template Method design pattern (see Inner Classes Thinking in Patterns (with Java) at www.MindView.net). The Template Method contains the basic structure of the algorithm, and it calls one or more overrideable methods to complete the action of that algorithm. A design pattern separates things that change from things that stay the same, and in this case the Template Method is the part that stays the same, and the overrideable methods are the things that change. A control framework is a particular type of application framework dominated by the need to respond to events. A system that primarily responds to events is called an event-driven system. A common problem in application programming is the graphical user interface (GUI), which is almost entirely event-driven. As you will see in the Graphical User Interfaces chapter, the Java Swing library is a control framework that elegantly solves the GUI problem and that heavily uses inner classes. To see how inner classes allow the simple creation and use of control frameworks, consider a control framework whose job is to execute events whenever those events are "ready." Although "ready" could mean anything, in this case it will be based on clock time. What follows is a control framework that contains no specific information about what it’s controlling. That information is supplied during inheritance, when the action( ) portion of the algorithm is implemented. First, here is the interface that describes any control event. It’s an abstract class instead of an actual interface because the default behavior is to perform the control based on time. Thus, some of the implementation is included here:
```java
//: innerclasses/controller/Event.java
// The common methods for any control event.
package innerclasses.controller;
public abstract class Event {
private long eventTime;
protected final long delayTime;
public Event(long delayTime) {
this.delayTime = delayTime;
start();
}
public void start() { // Allows restarting
eventTime = System.nanoTime() + delayTime;
}
public boolean ready() {
return System.nanoTime() >= eventTime;
}
public abstract void action();
} ///:~
```

<!--p287-->
The constructor captures the time (measured from the time of creation of the object) when you want the Event to run, and then calls start( ), which takes the current time and adds the delay time to produce the time when the event will occur. Rather than being included in the constructor, start( ) is a separate method. This way, you can restart the timer after the event has run out, so the Event object can be reused. For example, if you want a repeating event, you can simply call start( ) inside your action( ) method. ready( ) tells you when it’s time to run the action( ) method. Of course, ready( ) can be overridden in a derived class to base the Event on something other than time. The following file contains the actual control framework that manages and fires events. The Event objects are held inside a container object of type List<Event> (pronounced "List of Event"), which you’ll learn more about in the Holding Your Objects chapter. For now, all you need to know is that add( ) will append an Event to the end of the List, size( ) produces Inner Classes the number of entries in the List, the foreach syntax fetches successive Events from the List, and remove( ) removes the specified Event from the List.
```java
//: innerclasses/controller/Controller.java
// The reusable framework for control systems.
package innerclasses.controller;
import java.util.*;
public class Controller {
// A class from java.util to hold Event objects:
private List<Event> eventList = new ArrayList<Event>();
public void addEvent(Event c) { eventList.add(c); }
public void run() {
while(eventList.size() > 0)
// Make a copy so you’re not modifying the list
// while you’re selecting the elements in it:
for(Event e : new ArrayList<Event>(eventList))
if(e.ready()) {
System.out.println(e);
e.action();
eventList.remove(e);
}
}
} ///:~
```

<!--p288-->
The run( ) method loops through a copy of the eventList, hunting for an Event object that’s ready( ) to run. For each one it finds ready( ), it prints information using the object’s toString( ) method, calls the action( ) method, and then removes the Event from the list. Note that so far in this design you know nothing about exactly what an Event does. And this is the crux of the design—how it "separates the things that change from the things that stay the same." Or, to use my term, the "vector of change" is the different actions of the various kinds of Event objects, and you express different actions by creating different Event subclasses. This is where inner classes come into play. They allow two things: 1. The entire implementation of a control framework is created in a single class, thereby encapsulating everything that’s unique about that implementation. Inner classes are used to express the many different kinds of action( ) necessary to solve the problem. 2.Inner classes keep this implementation from becoming awkward, since you’re able to easily access any of the members in the outer class. Without this ability the code might become unpleasant enough that you’d end up seeking an alternative. Consider a particular implementation of the control framework designed to control greenhouse functions.4 Each action is entirely different: turning lights, water, and thermostats on and off, ringing bells, and restarting the system. But the control framework is designed to easily isolate this different code. Inner classes allow you to have multiple derived versions of the same base class, Event, within a single class. For each type of action, you inherit a new Event inner class, and write the control code in the action( ) implementation. As is typical with an application framework, the class GreenhouseControls is inherited from Controller: 4For some reason this has always been a pleasing problem for me to solve; it came from my earlier book C++ Inside & Out, but Java allows a more elegant solution

<!--p289-->
```java
//: innerclasses/GreenhouseControls.java
// This produces a specific application of the
// control system, all in a single class. Inner
// classes allow you to encapsulate different
// functionality for each type of event.
import innerclasses.controller.*;
public class GreenhouseControls extends Controller {
private boolean light = false;
public class LightOn extends Event {
public LightOn(long delayTime) { super(delayTime); }
public void action() {
// Put hardware control code here to
// physically turn on the light.
light = true;
}
public String toString() { return "Light is on"; }
}
public class LightOff extends Event {
public LightOff(long delayTime) { super(delayTime); }
public void action() {
// Put hardware control code here to
// physically turn off the light.
light = false;
}
public String toString() { return "Light is off"; }
}
private boolean water = false;
public class WaterOn extends Event {
public WaterOn(long delayTime) { super(delayTime); }
public void action() {
// Put hardware control code here.
water = true;
}
public String toString() {
return "Greenhouse water is on";
}
}
public class WaterOff extends Event {
public WaterOff(long delayTime) { super(delayTime); }
public void action() {
// Put hardware control code here.
water = false;
}
public String toString() {
return "Greenhouse water is off";
}
}
private String thermostat = "Day";
public class ThermostatNight extends Event {
public ThermostatNight(long delayTime) {
super(delayTime);
}
public void action() {
// Put hardware control code here.
thermostat = "Night";
}
public String toString() {
return "Thermostat on night setting";
}
}
public class ThermostatDay extends Event {
public ThermostatDay(long delayTime) {
super(delayTime);
}
public void action() {
// Put hardware control code here.
thermostat = "Day";
}
public String toString() {
return "Thermostat on day setting";
}
}
// An example of an action() that inserts a
// new one of itself into the event list:
public class Bell extends Event {
public Bell(long delayTime) { super(delayTime); }
public void action() {
addEvent(new Bell(delayTime));
}
public String toString() { return "Bing!"; }
}
public class Restart extends Event {
private Event[] eventList;
public Restart(long delayTime, Event[] eventList) {
super(delayTime);
this.eventList = eventList;
for(Event e : eventList)
addEvent(e);
}
public void action() {
for(Event e : eventList) {
e.start(); // Rerun each event
addEvent(e);
}
start(); // Rerun this Event
addEvent(this);
}
public String toString() {
return "Restarting system";
}
}
public static class Terminate extends Event {
public Terminate(long delayTime) { super(delayTime); }
public void action() { System.exit(0); }
public String toString() { return "Terminating"; }
}
} ///:~
```

<!--p290-->
Note that light, water, and thermostat belong to the outer class GreenhouseControls, and yet the inner classes can access those fields without qualification or special permission. Also, the action( ) methods usually involve some sort of hardware control. Most of the Event classes look similar, but Bell and Restart are special. Bell rings and then adds a new Bell object to the event list, so it will ring again later. Notice how inner classes almost look like multiple inheritance: Bell and Restart have all the methods of Event and also appear to have all the methods of the outer class GreenhouseControls. Restart is given an array of Event objects that it adds to the controller. Since Restart( ) is just another Event object, you can also add a Restart object within Restart.action( ) so that the system regularly restarts itself. Inner Classes The following class configures the system by creating a GreenhouseControls object and adding various kinds of Event objects. This is an example of the Command design pattern— each object in eventList is a request encapsulated as an object:
```java
//: innerclasses/GreenhouseController.java
// Configure and execute the greenhouse system.
// {Args: 5000}
import innerclasses.controller.*;
public class GreenhouseController {
public static void main(String[] args) {
GreenhouseControls gc = new GreenhouseControls();
// Instead of hard-wiring, you could parse
// configuration information from a text file here:
gc.addEvent(gc.new Bell(900));
Event[] eventList = {
gc.new ThermostatNight(0),
gc.new LightOn(200),
gc.new LightOff(400),
gc.new WaterOn(600),
gc.new WaterOff(800),
gc.new ThermostatDay(1400)
};
gc.addEvent(gc.new Restart(2000, eventList));
if(args.length == 1)
gc.addEvent(
new GreenhouseControls.Terminate(
new Integer(args[0])));
gc.run();
}
} /* Output:
Bing!
Thermostat on night setting
Light is on
Light is off
Greenhouse water is on
Greenhouse water is off
Thermostat on day setting
Restarting system
Terminating
*///:~
```

<!--p291-->
This class initializes the system, so it adds all the appropriate events. The Restart event is repeatedly run, and it loads the eventList into the GreenhouseControls object each time. If you provide a command-line argument indicating milliseconds, it will terminate the program after that many milliseconds (this is used for testing). Of course, it’s more flexible to read the events from a file instead of hardcoding them. An exercise in the I/O chapter asks you to modify this example to do just that. This example should move you toward an appreciation of the value of inner classes, especially when used within a control framework. However, in the Graphical User Interfaces chapter you’ll see how elegantly inner classes are used to describe the actions of a graphical user interface. By the time you finish that chapter, you should be fully convinced. Exercise 24:(2) In GreenhouseControls.java, add Event inner classes that turn fans on and off. Configure GreenhouseController.java to use these new Event objects. Exercise 25:(3) Inherit from GreenhouseControls in GreenhouseControls.java to add Event inner classes that turn water mist generators on and off. Write a new version of GreenhouseController.java to use these new Event objects. Inheriting from inner classes Because the inner-class constructor must attach to a reference of the enclosing class object, things are slightly complicated when you inherit from an inner class. The problem is that the "secret" reference to the enclosing class object must be initialized, and yet in the derived class there’s no longer a default object to attach to. You must use a special syntax to make the association explicit:
```java
//: innerclasses/InheritInner.java
// Inheriting an inner class.
class WithInner {
class Inner {}
}
public class InheritInner extends WithInner.Inner {
//! InheritInner() {} // Won’t compile
InheritInner(WithInner wi) {
wi.super();
}
public static void main(String[] args) {
WithInner wi = new WithInner();
InheritInner ii = new InheritInner(wi);
}
} ///:~
```
You can see that InheritInner is extending only the inner class, not the outer one. But when it comes time to create a constructor, the default one is no good, and you can’t just pass a reference to an enclosing object. In addition, you must use the syntax
```java
enclosingClassReference.super();
```
inside the constructor. This provides the necessary reference, and the program will then compile. Exercise 26:(2) Create a class with an inner class that has a non-default constructor (one that takes arguments). Create a second class with an inner class that inherits from the first inner class. Can inner classes be overridden? What happens when you create an inner class, then inherit from the enclosing class and redefine the inner class? That is, is it possible to "override" the entire inner class? This seems like it would be a powerful concept, but "overriding" an inner class as if it were another method of the outer class doesn’t really do anything:
```java
//: innerclasses/BigEgg.java
// An inner class cannot be overriden like a method.
import static net.mindview.util.Print.*;
class Egg {
private Yolk y;
```

<!--p292-->
Inner Classes
```java
protected class Yolk {
public Yolk() { print("Egg.Yolk()"); }
}
public Egg() {
print("New Egg()");
y = new Yolk();
}
}
public class BigEgg extends Egg {
public class Yolk {
public Yolk() { print("BigEgg.Yolk()"); }
}
public static void main(String[] args) {
new BigEgg();
}
} /* Output:
New Egg()
Egg.Yolk()
*///:~
```
The default constructor is synthesized automatically by the compiler, and this calls the base- class default constructor. You might think that since a BigEgg is being created, the "overridden" version of Yolk would be used, but this is not the case, as you can see from the output. This example shows that there isn’t any extra inner-class magic going on when you inherit from the outer class. The two inner classes are completely separate entities, each in its own namespace. However, it’s still possible to explicitly inherit from the inner class:

<!--p293-->
```java
//: innerclasses/BigEgg2.java
// Proper inheritance of an inner class.
import static net.mindview.util.Print.*;
class Egg2 {
protected class Yolk {
public Yolk() { print("Egg2.Yolk()"); }
public void f() { print("Egg2.Yolk.f()");}
}
private Yolk y = new Yolk();
public Egg2() { print("New Egg2()"); }
public void insertYolk(Yolk yy) { y = yy; }
public void g() { y.f(); }
}
public class BigEgg2 extends Egg2 {
public class Yolk extends Egg2.Yolk {
public Yolk() { print("BigEgg2.Yolk()"); }
public void f() { print("BigEgg2.Yolk.f()"); }
}
public BigEgg2() { insertYolk(new Yolk()); }
public static void main(String[] args) {
Egg2 e2 = new BigEgg2();
e2.g();
}
} /* Output:
Egg2.Yolk()
New Egg2()
Egg2.Yolk()
BigEgg2.Yolk()
BigEgg2.Yolk.f()
*///:~
```
Now BigEgg2.Yolk explicitly extends Egg2.Yolk and overrides its methods. The method insertYolk( ) allows BigEgg2 to upcast one of its own Yolk objects into the y reference in Egg2, so when g( ) calls y.f( ), the overridden version of f( ) is used. The second call to Egg2.Yolk( ) is the base-class constructor call of the BigEgg2.Yolk constructor. You can see that the overridden version of f( ) is used when g( ) is called. Local inner classes As noted earlier, inner classes can also be created inside code blocks, typically inside the body of a method. A local inner class cannot have an access specifier because it isn’t part of the outer class, but it does have access to the final variables in the current code block and all the members of the enclosing class. Here’s an example comparing the creation of a local inner class with an anonymous inner class:
```java
//: innerclasses/LocalInnerClass.java
// Holds a sequence of Objects.
import static net.mindview.util.Print.*;
interface Counter {
int next();
}
public class LocalInnerClass {
private int count = 0;
Counter getCounter(final String name) {
// A local inner class:
class LocalCounter implements Counter {
public LocalCounter() {
// Local inner class can have a constructor
print("LocalCounter()");
}
public int next() {
printnb(name); // Access local final
return count++;
}
}
return new LocalCounter();
}
// The same thing with an anonymous inner class:
Counter getCounter2(final String name) {
return new Counter() {
// Anonymous inner class cannot have a named
// constructor, only an instance initializer:
{
print("Counter()");
}
public int next() {
printnb(name); // Access local final
return count++;
}
};
}
public static void main(String[] args) {
LocalInnerClass lic = new LocalInnerClass();
Counter
c1 = lic.getCounter("Local inner "),
c2 = lic.getCounter2("Anonymous inner ");
for(int i = 0; i < 5; i++)
print(c1.next());
for(int i = 0; i < 5; i++)
```

<!--p294-->
Inner Classes
```java
print(c2.next());
}
} /* Output:
LocalCounter()
Counter()
Local inner 0
Local inner 1
Local inner 2
Local inner 3
Local inner 4
Anonymous inner 5
Anonymous inner 6
Anonymous inner 7
Anonymous inner 8
Anonymous inner 9
*///:~
```
Counter returns the next value in a sequence. It is implemented as both a local class and an anonymous inner class, both of which have the same behaviors and capabilities. Since the name of the local inner class is not accessible outside the method, the only justification for using a local inner class instead of an anonymous inner class is if you need a named constructor and/or an overloaded constructor, since an anonymous inner class can only use instance initialization. Another reason to make a local inner class rather than an anonymous inner class is if you need to make more than one object of that class. Inner-class identifiers Since every class produces a .class file that holds all the information about how to create objects of this type (this information produces a "meta-class" called the Class object), you might guess that inner classes must also produce .classfiles to contain the information for their Class objects. The names of these files/classes have a strict formula: the name of the enclosing class, followed by a ‘$’, followed by the name of the inner class. For example, the .class files created by LocalInnerClass.java include:
```java
Counter.class
LocalInnerClass$l.class
LocallnnerClassSlLocalCounter.class
LocallnnerClass.class
```

<!--p295-->
If inner classes are anonymous, the compiler simply starts generating numbers as inner-class identifiers. If inner classes are nested within inner classes, their names are simply appended after a ‘$’ and the outer-class identifier (s). Although this scheme of generating internal names is simple and straightforward, it’s also robust and handles most situations.5Since it is the standard naming scheme for Java, the generated files are automatically platform-independent. (Note that the Java compiler is changing your inner classes in all sorts of other ways in order to make them work.) 5On the other hand, ‘$’ is a meta-character to the Unix shell and so you’ll sometimes have trouble when listing the .class files. This is a bit strange coming from Sun, a Unix-based company. My guess is that they weren’t considering this issue, but instead thought you’d naturally focus on the source-code files. Inner Classes Summary Interfaces and inner classes are more sophisticated concepts than what you’ll find in many OOP languages; for example, there’s nothing like them in C++. Together, they solve the same problem that C++ attempts to solve with its multiple inheritance (MI) feature. However, MI in C++ turns out to be rather difficult to use, whereas Java interfaces and inner classes are, by comparison, much more accessible. Although the features themselves are reasonably straightforward, the use of these features is a design issue, much the same as polymorphism. Over time, you’ll become better at recognizing situations where you should use an interface, or an inner class, or both. But at this point in this book, you should at least be comfortable with the syntax and semantics. As you see these language features in use, you’ll eventually internalize them. Solutions to selected exercises can be found in the electronic document The Thinking in Java Annotated Solution Guide, available for sale from www.MindView.net.