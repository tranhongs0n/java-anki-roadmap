# 9. Interfaces (printed p219-242)


<!--p241-->
Interfaces Interfaces and abstract classes provide more structured way to separate interface from implementation. Such mechanisms are not that common in programming languages. C++, for example, only has indirect support for these concepts. The fact that language keywords exist in Java indicates that these ideas were considered important enough to provide direct support. First, we’ll look at the abstract class, which is a kind of midway step between an ordinary class and an interface. Although your first impulse will be to create an interface, the abstract class is an important and necessary tool for building classes that have some unimplemented methods. You can’t always use a pure interface. Abstract classes and methods In all the “instrument” examples in the previous chapter, the methods in the base class Instrument were always “dummy” methods. If these methods are ever called, you’ve done something wrong. That’s because the intent of Instrument is to create a common interface for all the classes derived from it. In those examples, the only reason to establish this common interface is so that it can be expressed differently for each different subtype. It establishes a basic form, so that you can say what’s common for all the derived classes. Another way of saying this is to call Instrument an abstract base class, or simply an abstract class. If you have an abstract class like Instrument, objects of that specific class almost always have no meaning. You create an abstract class when you want to manipulate a set of classes through its common interface. Thus, Instrument is meant to express only the interface, and not a particular implementation, so creating an Instrument object makes no sense, and you’ll probably want to prevent the user from doing it. This can be accomplished by making all methods in Instrument generate errors, but that delays the information until run time and requires reliable exhaustive testing on the user’s part. It’s usually better to catch problems at compile time. Java provides a mechanism for doing this called the abstract method.1 This is a method that is incomplete; it has only a declaration and no method body. Here is the syntax for an abstract method declaration.
```java
abstract void f( );
```

<!--p242-->
A class containing abstract methods is called an abstract class. If a class contains one or more abstract methods, the class itself must be qualified as abstract. (Otherwise, the compiler gives you an error message.) If an abstract class is incomplete, what is the compiler supposed to do when someone tries to make an object of that class? It cannot safely create an object of an abstract class, so you get 1For C++ programmers, this ist he analogue of C++’s pure virtual function. an error message from the compiler. This way, the compiler ensures the purity of the abstract class, and you don’t need to worry about misusing it. If you inherit from an abstract class and you want to make objects of the new type, you must provide method definitions for all the abstract methods in the base class. If you don’t (and you may choose not to), then the derived class is also abstract, and the compiler will force you to qualify that class with the abstract keyword. It’s possible to make a class abstract without including any abstract methods. This is useful when you’ve got a class in which it doesn’t make sense to have any abstract methods, and yet you want to prevent any instances of that class. The Instrument class from the previous chapter can easily be turned into an abstract class. Only some of the methods will be abstract, since making a class abstract doesn’t force you to make all the methods abstract. Here’s what it looks like: Here’s the orchestra example modified to use abstract classes and methods:

<!--p243-->
```java
//: interfaces/music4/Music4.java
// Abstract classes and methods.
package interfaces.music4;
import polymorphism.music.Note;
import static net.mindview.util.Print.*;
abstract class Instrument {
private int i; // Storage allocated for each
public abstract void play(Note n);
public String what() { return "Instrument"; }
public abstract void adjust();
}
class Wind extends Instrument {
public void play(Note n) {
print("Wind.play() " + n);
}
public String what() { return "Wind"; }
public void adjust() {}
}
class Percussion extends Instrument {
public void play(Note n) {
print("Percussion.play() " + n);
}
public String what() { return "Percussion"; }
public void adjust() {}
}
class Stringed extends Instrument {
public void play(Note n) {
print("Stringed.play() " + n);
}
public String what() { return "Stringed"; }
public void adjust() {}
}
class Brass extends Wind {
public void play(Note n) {
print("Brass.play() " + n);
}
public void adjust() { print("Brass.adjust()"); }
}
class Woodwind extends Wind {
public void play(Note n) {
print("Woodwind.play() " + n);
}
public String what() { return "Woodwind"; }
}
public class Music4 {
// Doesn’t care about type, so new types
// added to the system still work right:
static void tune(Instrument i) {
// ...
i.play(Note.MIDDLE_C);
}
static void tuneAll(Instrument[] e) {
for(Instrument i : e)
tune(i);
}
public static void main(String[] args) {
// Upcasting during addition to the array:
Instrument[] orchestra = {
new Wind(),
new Percussion(),
new Stringed(),
new Brass(),
new Woodwind()
};
```

<!--p244-->
Interfaces
```java
tuneAll(orchestra);
}
} /* Output:
Wind.play() MIDDLE_C
Percussion.play() MIDDLE_C
Stringed.play() MIDDLE_C
Brass.play() MIDDLE_C
Woodwind.play() MIDDLE_C
*///:~
```

<!--p245-->

<!--p246-->
You can see that there’s really no change except in the base class. It’s helpful to create abstract classes and methods because they make the abstractness of a class explicit, and tell both the user and the compiler how it was intended to be used. Abstract classes are also useful refactoring tolls, since they allow you to easily move common methods up the inheritance hierarchy. Exercise 1: (1) Modify Exercise 9 in the previous chapter so that Rodent is an abstract class. Make the methods of Rodent abstract whenever possible. Exercise 2: (1) Create a class as abstract without including any abstract methods and verify that you cannot create any instances of that class. Exercise 3: (2) Create a base class with an abstractprint( ) method that is overridden in a derived class. The overridden version of the method prints the value of an int variable defined in the derived class. At the point of definition of this variable, give it a nonzero value. In the base-class constructor, call this method. In main( ), create an object of the derived type, and then call its print( ) method. Explain the results. Exercise 4: (3) Create an abstract class with no methods. Derive a class and add a method. Create a static method that takes a reference to the base class, downcasts it to the derived class, and calls the method. In main( ), demonstrate that it works. Now put the abstract declaration for the method in the base class, thus eliminating the need for the downcast. Interfaces The interface keyword takes the concept of abstractness one step further. The abstract keyword allows you to create one or more undefined methods in a class—you provide part of the interface without providing a corresponding implementation. The implementation is provided by inheritors. The interface keyword produces a completely abstract class, one that provides no implementation at all. It allows the creator to determine method names, argument lists, and return types, but no method bodies. An interface provides only a form, but no implementation. An interface says, "All classes that implement this particular interface will look like this." Thus, any code that uses a particular interface knows what methods might be called for that interface, and that’s all. So the interface is used to establish a "protocol" between classes. (Some object-oriented programming languages have a keyword called protocol to do the same thing.) However, an interface is more than just an abstract class taken to the extreme, since it allows you to perform a variation of "multiple inheritance" by creating a class that can be upcast to more than one base type. To create an interface, use the interface keyword instead of the class keyword. As with a class, you can add the public keyword before the interface keyword (but only if that interface is defined in a file of the same name). If you leave off the public keyword, you get package access, so the interface is only usable within the same package. An interface can also contain fields, but these are implicitly static and final. To make a class that conforms to a particular interface (or group of interfaces), use the implements keyword, which says, "The interface is what it looks like, but now I’m going to say how it works." Other than that, it looks like inheritance. The diagram for the instrument example shows this: You can see from the Woodwind and Brass classes that once you’ve implemented an interface, that implementation becomes an ordinary class that can be extended in the regular way. You can choose to explicitly declare the methods in an interface as public, but they are public even if you don’t say it. So when you implement an interface, the methods from the interface must be defined as public. Otherwise, they would default to package access, and you’d be reducing the accessibility of a method during inheritance, which is not allowed by the Java compiler. You can see this in the modified version of the Instrument example. Note that every method in the interface is strictly a declaration, which is the only thing the compiler allows. In addition, none of the methods in Instrument are declared as public, but they’re automatically public anyway: Interfaces

<!--p247-->
```java
//: interfaces/music5/Music5.java
// Interfaces.
package interfaces.music5;
import polymorphism.music.Note;
import static net.mindview.util.Print.*;
interface Instrument {
// Compile-time constant:
int VALUE = 5; // static & final
// Cannot have method definitions:
void play(Note n); // Automatically public
void adjust();
}
class Wind implements Instrument {
public void play(Note n) {
print(this + ".play() " + n);
}
public String toString() { return "Wind"; }
public void adjust() { print(this + ".adjust()"); }
}
class Percussion implements Instrument {
public void play(Note n) {
print(this + ".play() " + n);
}
public String toString() { return "Percussion"; }
public void adjust() { print(this + ".adjust()"); }
}
class Stringed implements Instrument {
public void play(Note n) {
print(this + ".play() " + n);
}
public String toString() { return "Stringed"; }
public void adjust() { print(this + ".adjust()"); }
}
class Brass extends Wind {
public String toString() { return "Brass"; }
}
class Woodwind extends Wind {
public String toString() { return "Woodwind"; }
}
public class Music5 {
// Doesn’t care about type, so new types
// added to the system still work right:
static void tune(Instrument i) {
// ...
i.play(Note.MIDDLE_C);
}
static void tuneAll(Instrument[] e) {
for(Instrument i : e)
tune(i);
}
public static void main(String[] args) {
// Upcasting during addition to the array:
Instrument[] orchestra = {
new Wind(),
new Percussion(),
new Stringed(),
new Brass(),
new Woodwind()
};
tuneAll(orchestra);
}
} /* Output:
Wind.play() MIDDLE_C
Percussion.play() MIDDLE_C
Stringed.play() MIDDLE_C
Brass.play() MIDDLE_C
Woodwind.play() MIDDLE_C
*///:~
```
One other change has been made to this version of the example: The what( ) method has been changed to toString( ), since that was how the method was being used. Since toString( ) is part of the root class Object, it doesn’t need to appear in the interface. The rest of the code works the same. Notice that it doesn’t matter if you are upcasting to a "regular" class called Instrument, an abstract class called Instrument, or to an interface called Instrument. The behavior is the same. In fact, you can see in the tune( ) method that there isn’t any evidence about whether Instrument is a "regular" class, an abstract class, or an interface. Exercise 5:(2) Create an interface containing three methods, in its own package. Implement the interface in a different package. Exercise 6:(2) Prove that all the methods in an interface are automatically public. Exercise 7: (1) Change Exercise 9 in the Polymorphism chapter so that Rodent is an interface. Exercise 8:(2) In polymorphism.Sandwich.java, create an interface called FastFoo d (with appropriate methods) and change Sandwic h so that it also implements FastFood. Exercise 9:(3) Refactor Musics.java by moving the common methods in Wind, Percussion and Stringed into an abstract class. Exercise 10:(3) Modify Musics.java by adding a Playable interface. Move the play( ) declaration from Instrument to Playable. Add Playable to the derived classes by including it in the implement s list. Change tune( ) so that it takes a Playable instead of an Instrument. Complete decoupling Whenever a method works with a class instead of an interface, you are limited to using that class or its subclasses. If you would like to apply the method to a class that isn’t in that hierarchy, you’re out of luck. An interface relaxes this constraint considerably. As a result, it allows you to write more reusable code. For example, suppose you have a Processor class that has a name( ) and a process( ) method that takes input, modifies it and produces output. The base class is extended to create different types of Processor. In this case, the Processor subtypes modify String objects (note that the return types can be covariant, but not the argument types):
```java
//: interfaces/classprocessor/Apply.java
```

<!--p248-->
Interfaces
```java
package interfaces.classprocessor;
import java.util.*;
import static net.mindview.util.Print.*;
class Processor {
public String name() {
return getClass().getSimpleName();
}
Object process(Object input) { return input; }
}
class Upcase extends Processor {
String process(Object input) { // Covariant return
return ((String)input).toUpperCase();
}
}
class Downcase extends Processor {
String process(Object input) {
return ((String)input).toLowerCase();
}
}
class Splitter extends Processor {
String process(Object input) {
// The split() argument divides a String into pieces:
return Arrays.toString(((String)input).split(" "));
}
}
public class Apply {
public static void process(Processor p, Object s) {
print("Using Processor " + p.name());
print(p.process(s));
}
public static String s =
"Disagreement with beliefs is by definition incorrect";
public static void main(String[] args) {
process(new Upcase(), s);
process(new Downcase(), s);
process(new Splitter(), s);
}
} /* Output:
Using Processor Upcase
DISAGREEMENT WITH BELIEFS IS BY DEFINITION INCORRECT
Using Processor Downcase
disagreement with beliefs is by definition incorrect
Using Processor Splitter
[Disagreement, with, beliefs, is, by, definition, incorrect]
*///:~
```

<!--p249-->
The Apply.process( ) method takes any kind of Processor and applies it to an Object, then prints the results. Creating a method that behaves differently depending on the argument object that you pass it is called the Strategy design pattern. The method contains the fixed part of the algorithm to be performed, and the Strategy contains the part that varies. The Strategy is the object that you pass in, and it contains code to be executed. Here, the Processor object is the Strategy, and in main( ) you can see three different Strategies applied to the String s. The split( ) method is part of the String class. It takes the String object and splits it using the argument as a boundary, and returns a String[]. It is used here as a shorter way of creating an array of String. Now suppose you discover a set of electronic filters that seem like they could fit into your Apply.process( ) method:
```java
//: interfaces/filters/Waveform.java
package interfaces.filters;
public class Waveform {
private static long counter;
private final long id = counter++;
public String toString() { return "Waveform " + id; }
} ///:~
//: interfaces/filters/Filter.java
package interfaces.filters;
public class Filter {
public String name() {
return getClass().getSimpleName();
}
public Waveform process(Waveform input) { return input; }
} ///:~
//: interfaces/filters/LowPass.java
package interfaces.filters;
public class LowPass extends Filter {
double cutoff;
public LowPass(double cutoff) { this.cutoff = cutoff; }
public Waveform process(Waveform input) {
return input; // Dummy processing
}
} ///:~
//: interfaces/filters/HighPass.java
package interfaces.filters;
public class HighPass extends Filter {
double cutoff;
public HighPass(double cutoff) { this.cutoff = cutoff; }
public Waveform process(Waveform input) { return input; }
} ///:~
//: interfaces/filters/BandPass.java
package interfaces.filters;
public class BandPass extends Filter {
double lowCutoff, highCutoff;
public BandPass(double lowCut, double highCut) {
lowCutoff = lowCut;
highCutoff = highCut;
}
public Waveform process(Waveform input) { return input; }
} ///:~
```

<!--p250-->
Filter has the same interface elements as Processor, but because it isn’t inherited from Processor—because the creator of the Filter class had no clue you might want to use it as a Processor—you can’t use a Filter with the Apply.process( ) method, even though it would work fine. Basically, the coupling between Apply.process( ) and Processor is stronger than it needs to be, and this prevents the Apply.process( ) code from being reused when it ought to be. Also notice that the inputs and outputs are both Waveforms. Interfaces If Processor is an interface, however, the constraints are loosened enough that you can reuse an Apply.process( ) that takes that interface. Here are the modified versions of Processor and Apply:
```java
//: interfaces/interfaceprocessor/Processor.java
package interfaces.interfaceprocessor;
public interface Processor {
String name();
Object process(Object input);
} ///:~
//: interfaces/interfaceprocessor/Apply.java
package interfaces.interfaceprocessor;
import static net.mindview.util.Print.*;
public class Apply {
public static void process(Processor p, Object s) {
print("Using Processor " + p.name());
print(p.process(s));
}
} ///:~
```
The first way you can reuse code is if client programmers can write their classes to conform to the interface, like this:

<!--p251-->
```java
//: interfaces/interfaceprocessor/StringProcessor.java
package interfaces.interfaceprocessor;
import java.util.*;
public abstract class StringProcessor implements Processor{
public String name() {
return getClass().getSimpleName();
}
public abstract String process(Object input);
public static String s =
"If she weighs the same as a duck, she’s made of wood";
public static void main(String[] args) {
Apply.process(new Upcase(), s);
Apply.process(new Downcase(), s);
Apply.process(new Splitter(), s);
}
}
class Upcase extends StringProcessor {
public String process(Object input) { // Covariant return
return ((String)input).toUpperCase();
}
}
class Downcase extends StringProcessor {
public String process(Object input) {
return ((String)input).toLowerCase();
}
}
class Splitter extends StringProcessor {
public String process(Object input) {
return Arrays.toString(((String)input).split(" "));
}
} /* Output:
Using Processor Upcase
IF SHE WEIGHS THE SAME AS A DUCK, SHE’S MADE OF WOOD
Using Processor Downcase
if she weighs the same as a duck, she’s made of wood
Using Processor Splitter
[If, she, weighs, the, same, as, a, duck,, she’s, made, of, wood]
*///:~
```
However, you are often in the situation of not being able to modify the classes that you want to use. In the case of the electronic filters, for example, the library was discovered rather than created. In these cases, you can use the Adapter design pattern. In Adapter, you write code to take the interface that you have and produce the interface that you need, like this:
```java
//: interfaces/interfaceprocessor/FilterProcessor.java
package interfaces.interfaceprocessor;
import interfaces.filters.*;
class FilterAdapter implements Processor {
Filter filter;
public FilterAdapter(Filter filter) {
this.filter = filter;
}
public String name() { return filter.name(); }
public Waveform process(Object input) {
return filter.process((Waveform)input);
}
}
public class FilterProcessor {
public static void main(String[] args) {
Waveform w = new Waveform();
Apply.process(new FilterAdapter(new LowPass(1.0)), w);
Apply.process(new FilterAdapter(new HighPass(2.0)), w);
Apply.process(
new FilterAdapter(new BandPass(3.0, 4.0)), w);
}
} /* Output:
Using Processor LowPass
Waveform 0
Using Processor HighPass
Waveform 0
Using Processor BandPass
Waveform 0
*///:~
```

<!--p252-->
In this approach to Adapter, the FilterAdapter constructor takes the interface that you have—Filter—and produces an object that has the Processor interface that you need. You may also notice delegation in the FilterAdapter class. Decoupling interface from implementation allows an interface to be applied to multiple different implementations, and thus your code is more reusable. Exercise 11: (4) Create a class with a method that takes a String argument and produces a result that swaps each pair of characters in that argument. Adapt the class so that it works with interfaceprocessor.Apply.process( ). Interfaces “Multiple inheritance” in Java Because an interface has no implementation at all—that is, there is no storage associated with an interface—there’s nothing to prevent many interfaces from being combined. This is valuable because there are times when you need to say, "An x is an a and a b and a c." In C++, this act of combining multiple class interfaces is called multiple inheritance, and it carries some rather sticky baggage because each class can have an implementation. In Java, you can perform the same act, but only one of the classes can have an implementation, so the C++ problems do not occur with Java when combining multiple interfaces: In a derived class, you aren’t forced to have a base class that is either abstract or "concrete" (one with no abstract methods). If you do inherit from a non-interface, you can inherit from only one. All the rest of the base elements must be interfaces. You place all the interface names after the implements keyword and separate them with commas. You can have as many interfaces as you want. You can upcast to each interface, because each interface is an independent type. The following example shows a concrete class combined with several interfaces to produce a new class:

<!--p253-->
```java
//: interfaces/Adventure.java
// Multiple interfaces.
interface CanFight {
void fight();
}
interface CanSwim {
void swim();
}
interface CanFly {
void fly();
}
class ActionCharacter {
public void fight() {}
}
class Hero extends ActionCharacter
implements CanFight, CanSwim, CanFly {
public void swim() {}
public void fly() {}
}
public class Adventure {
public static void t(CanFight x) { x.fight(); }
public static void u(CanSwim x) { x.swim(); }
```
Interfaces
```java
public static void v(CanFly x) { x.fly(); }
public static void w(ActionCharacter x) { x.fight(); }
public static void main(String[] args) {
Hero h = new Hero();
t(h); // Treat it as a CanFight
u(h); // Treat it as a CanSwim
v(h); // Treat it as a CanFly
w(h); // Treat it as an ActionCharacter
}
} ///:~
```

<!--p254-->
You can see that Hero combines the concrete class ActionCharacter with the interfaces CanFight, CanSwim, and CanFly. When you combine a concrete class with interfaces this way, the concrete class must come first, then the interfaces. (The compiler gives an error otherwise.) The signature for fight( ) is the same in the interface CanFight and the class ActionCharacter, and that fight( ) is not provided with a definition in Hero. You can extend an interface, but then you’ve got another interface. When you want to create an object, all the definitions must first exist. Even though Hero does not explicitly provide a definition for fight( ), the definition comes along with ActionCharacter; thus, it’s possible to create Hero objects. In class Adventure, you can see that there are four methods that take arguments of the various interfaces and of the concrete class. When a Hero object is created, it can be passed to any of these methods, which means it is being upcast to each interface in turn. Because of the way interfaces are designed in Java, this works without any particular effort on the part of the programmer. Keep in mind that one of the core reasons for interfaces is shown in the preceding example: to upcast to more than one base type (and the flexibility that this provides). However, a second reason for using interfaces is the same as using an abstract base class: to prevent the client programmer from making an object of this class and to establish that it is only an interface. This brings up a question: Should you use an interface or an abstract class? If it’s possible to create your base class without any method definitions or member variables, you should always prefer interfaces to abstract classes. In fact, if you know something is going to be a base class, you can consider making it an interface (this subject will be revisited in the chapter summary). Exercise 12: (2) In Adventure.java, add an interface called CanClimb, following the form of the other interfaces. Exercise 13: (2) Create an interface, and inherit two new interfaces from that interface. Multiply inherit a third interface from the second two.2 Extending an interface with inheritance You can easily add new method declarations to an interface by using inheritance, and you can also combine several interfaces into a new interface with inheritance. In both cases you get a new interface, as seen in this example: 2This shows how interfaces prevent the "diamond problem" that occurs with C++ multiple inheritance.
```java
//: interfaces/HorrorShow.java
// Extending an interface with inheritance.
interface Monster {
void menace();
}
interface DangerousMonster extends Monster {
void destroy();
}
interface Lethal {
void kill();
}
class DragonZilla implements DangerousMonster {
public void menace() {}
public void destroy() {}
}
interface Vampire extends DangerousMonster, Lethal {
void drinkBlood();
}
class VeryBadVampire implements Vampire {
public void menace() {}
public void destroy() {}
public void kill() {}
public void drinkBlood() {}
}
public class HorrorShow {
static void u(Monster b) { b.menace(); }
static void v(DangerousMonster d) {
d.menace();
d.destroy();
}
static void w(Lethal l) { l.kill(); }
public static void main(String[] args) {
DangerousMonster barney = new DragonZilla();
u(barney);
v(barney);
Vampire vlad = new VeryBadVampire();
u(vlad);
v(vlad);
w(vlad);
}
} ///:~
```

<!--p255-->
DangerousMonster is a simple extension to Monster that produces a newinterface. This is implemented in DragonZilla. The syntax used in Vampire works only when inheriting interfaces. Normally, you can use extends with only a single class, but extends canrefer to multiple base interfaces when building a new interface. As you cansee, the interface names are simply separated with commas. Exercise 14:(2) Create three interfaces, each with two methods. Inherit anew interface that combines the three, adding a new method. Create a classby implementing the new interface and also inheriting from a concrete class. Now write four methods, each of which takes one of the four interfaces as anargument. In main( ), create an object of your class and pass it to each of themethods. Exercise 15:(2) Modify the previous exercise by creating an abstract class and inheriting that into the derived class. Name collisions when combining Interfaces You can encounter a small pitfall when implementing multiple interfaces. Inthe preceding example, both CanFight and ActionCharacter haveidentical void fight( ) methods. An identical method is not a problem, butwhat if the method differs by signature or return type? Here’s an example:
```java
//: interfaces/InterfaceCollision.java
package interfaces;
interface I1 { void f(); }
interface I2 { int f(int i); }
interface I3 { int f(); }
class C { public int f() { return 1; } }
class C2 implements I1, I2 {
public void f() {}
public int f(int i) { return 1; } // overloaded
}
class C3 extends C implements I2 {
public int f(int i) { return 1; } // overloaded
}
class C4 extends C implements I3 {
// Identical, no problem:
public int f() { return 1; }
}
// Methods differ only by return type:
//! class C5 extends C implements I1 {}
//! interface I4 extends I1, I3 {} ///:~
```

<!--p256-->
The difficulty occurs because overriding, implementation, and overloadingget unpleasantly mixed together. Also, overloaded methods cannot differ onlyby return type. When the last two lines are uncommented, the error messagessay it all: InterfaceCollision.java:23: f() in C cannot implementf() in It; attemptingto use incompatible return type found: int required: void InterfaceCollision.java:24: Interfaces I3 andh are incompatible; bothdefine f(), but with different return type Using the same method names in different interfaces that are intended to becombined generally causes confusion in the readability of the code, as well. Strive to avoid it. Interfaces Adapting to an interface One of the most compelling reasons for interfaces is to allow multipleimplementations for the same interface. In simple cases this is in the form of a method that accepts an interface, leaving it up to you to implement thatinterface and pass your object to the method. Thus, a common use for interfaces is the aforementioned Strategy designpattern. You write a method that performs certain operations, and thatmethod takes an interface that you also specify. You’re basically saying, "Youcan use my method with any object you like, as long as your object conformsto my interface." This makes your method more flexible, general and reusable. For example, the constructor for the Java SE5 Scanner class (which you’lllearn more about in the Strings chapter) takes a Readable interface. You’llfind that Readable is not an argument for any other method in the Javastandard library—it was created solely for Scanner, so that Scanner doesn’thave to constrain its argument to be a particular class. This way, Scanner can be made to work with more types. If you create a new class and you wantit to be usable with Scanner, you make it Readable, like this:

<!--p257-->
```java
//: interfaces/RandomWords.java
// Implementing an interface to conform to a method.
import java.nio.*;
import java.util.*;
public class RandomWords implements Readable {
private static Random rand = new Random(47);
private static final char[] capitals =
"ABCDEFGHIJKLMNOPQRSTUVWXYZ".toCharArray();
private static final char[] lowers =
"abcdefghijklmnopqrstuvwxyz".toCharArray();
private static final char[] vowels =
"aeiou".toCharArray();
private int count;
public RandomWords(int count) { this.count = count; }
public int read(CharBuffer cb) {
if(count-- == 0)
return -1; // Indicates end of input
cb.append(capitals[rand.nextInt(capitals.length)]);
for(int i = 0; i < 4; i++) {
cb.append(vowels[rand.nextInt(vowels.length)]);
cb.append(lowers[rand.nextInt(lowers.length)]);
}
cb.append(" ");
return 10; // Number of characters appended
}
public static void main(String[] args) {
Scanner s = new Scanner(new RandomWords(10));
while(s.hasNext())
System.out.println(s.next());
}
} /* Output:
Yazeruyac
Fowenucor
Goeazimom
Raeuuacio
Nuoadesiw
Hageaikux
Ruqicibui
Numasetih
Kuuuuozog
Waqizeyoy
*///:~
```
The Readable interface only requires the implementation of a read( ) method. Inside read( ), you add to the CharBuffer argument (there areseveral ways to do this; see the CharBuffer documentation), or return -lwhen you have no more input. Suppose you have a class that does not already implement Readable—howdo you make it work with Scanner? Here’s an example of a class thatproduces random floating point numbers:
```java
//: interfaces/RandomDoubles.java
import java.util.*;
public class RandomDoubles {
private static Random rand = new Random(47);
public double next() { return rand.nextDouble(); }
public static void main(String[] args) {
RandomDoubles rd = new RandomDoubles();
for(int i = 0; i < 7; i ++)
System.out.print(rd.next() + " ");
}
} /* Output:
0.7271157860730044 0.5309454508634242 0.16020656493302599
0.18847866977771732 0.5166020801268457 0.2678662084200585
0.2613610344283964
*///:~
```
Because you can add an interface onto any existing class in this way, it meansthat a method that takes an interface provides a way for any class to beadapted to work with that method. This is the power of using interfacesinstead of classes. Exercise 16:(3) Create a class that produces a sequence of chars. Adaptthis class so that it can be an input to a Scanner object. Fields in interfaces Because any fields you put into an interface are automatically static and final, the interface is a convenient tool for creating groups of constant values. Before Java SE5, this was the only way to produce the same effect as an enum in C or C++. So you will see pre-Java SE5 code like this:
```java
//: interfaces/Months.java
// Using interfaces to create groups of constants.
package interfaces;
public interface Months {
int
JANUARY = 1, FEBRUARY = 2, MARCH = 3,
APRIL = 4, MAY = 5, JUNE = 6, JULY = 7,
AUGUST = 8, SEPTEMBER = 9, OCTOBER = 10,
NOVEMBER = 11, DECEMBER = 12;
} ///:~
```

<!--p258-->
Notice the Java style of using all uppercase letters (with underscores toseparate multiple words in a single identifier) for static finals that haveconstant initializers. The fields in an interface are automatically public, sothat is not explicitly specified. Interfaces With Java SE5, you now have the much more powerful and flexible enum keyword, so it rarely makes sense to use interfaces for constants anymore. However, you will probably run across the old idiom on many occasions whenreading legacy code (the supplements for this book at www.MindView.netcontain a complete description of the pre-Java SE5 approach to producingenumerated types using interfaces). You can find more details about using enums in the Enumerated Types chapter. Exercise 17:(2) Prove that the fields in an interface are implicitly static and final. Initializing fields in interfaces Fields defined in interfaces cannot be "blank finals," but they can beinitialized with non- constant expressions. For example:
```java
//: interfaces/RandVals.java
// Initializing interface fields with
// non-constant initializers.
import java.util.*;
public interface RandVals {
Random RAND = new Random(47);
int RANDOM_INT = RAND.nextInt(10);
long RANDOM_LONG = RAND.nextLong() * 10;
float RANDOM_FLOAT = RAND.nextLong() * 10;
double RANDOM_DOUBLE = RAND.nextDouble() * 10;
} ///:~
```
Since the fields are static, they are initialized when the class is first loaded, which happens when any of the fields are accessed for the first time. Here’s asimple test:
```java
//: interfaces/TestRandVals.java
import static net.mindview.util.Print.*;
public class TestRandVals {
public static void main(String[] args) {
print(RandVals.RANDOM_INT);
print(RandVals.RANDOM_LONG);
print(RandVals.RANDOM_FLOAT);
print(RandVals.RANDOM_DOUBLE);
}
} /* Output:
-32032247016559954
-8.5939291E18
5.779976127815049
*///:~
```

<!--p259-->
The fields, of course, are not part of the interface. The values are stored in thestatic storage area for that interface. Interfaces Nesting interfaces Interfaces may be nested within classes and within other interfaces.3 Thisreveals a number of interesting features:
```java
//: interfaces/nesting/NestingInterfaces.java
package interfaces.nesting;
class A {
interface B {
void f();
}
public class BImp implements B {
public void f() {}
}
private class BImp2 implements B {
public void f() {}
}
public interface C {
void f();
}
class CImp implements C {
public void f() {}
}
private class CImp2 implements C {
public void f() {}
}
private interface D {
void f();
}
private class DImp implements D {
public void f() {}
}
public class DImp2 implements D {
public void f() {}
}
public D getD() { return new DImp2(); }
private D dRef;
public void receiveD(D d) {
dRef = d;
dRef.f();
}
}
interface E {
interface G {
void f();
}
// Redundant "public":
public interface H {
void f();
}
void g();
// Cannot be private within an interface:
//! private interface I {}
}
public class NestingInterfaces {
```

<!--p260-->
3Thanks to Martin Danner for asking about this during a seminar.
```java
public class BImp implements A.B {
public void f() {}
}
class CImp implements A.C {
public void f() {}
}
// Cannot implement a private interface except
// within that interface’s defining class:
//! class DImp implements A.D {
//! public void f() {}
//! }
class EImp implements E {
public void g() {}
}
class EGImp implements E.G {
public void f() {}
}
class EImp2 implements E {
public void g() {}
class EG implements E.G {
public void f() {}
}
}
public static void main(String[] args) {
A a = new A();
// Can’t access A.D:
//! A.D ad = a.getD();
// Doesn’t return anything but A.D:
//! A.DImp2 di2 = a.getD();
// Cannot access a member of the interface:
//! a.getD().f();
// Only another A can do anything with getD():
A a2 = new A();
a2.receiveD(a.getD());
}
} ///:~
```

<!--p261-->
The syntax for nesting an interface within a class is reasonably obvious. Justlike non-nested interfaces, these can have public or package-access visibility. As an added twist, interfaces can also be private, as seen in A.D (the samequalification syntax is used for nested interfaces as for nested classes). Whatgood is a private nested interface? You might guess that it can only beimplemented as a private inner class as in DImp, but A.DImp2 shows thatit can also be implemented as a public class. However, A.DImp2 can onlybe used as itself. You are not allowed to mention the fact that it implementsthe private interface D, so implementing a private interface is a way toforce the definition of the methods in that interface without adding any typeinformation (that is, without allowing any upcasting). The method getD( ) produces a further quandary concerning the private interface: It’sa public method that returns a reference to a private interface. What can you do with the return value of this method? In main( ), you can see several attempts to use the return value, all of which fail. The onlything that works is if the return value is handed to an object that haspermission to use it—in this case, another A, via the receiveD( ) method. Interface E shows that interfaces can be nested within each other. However, the rules about interfaces—in particular, that all interface elements must be public—are strictly enforced here, so an interface nested within anotherinterface is automatically public and cannot be made private. Nestinglnterfaces shows the various ways that nested interfaces can beimplemented. In particular, notice that when you implement an interface, you are not required to implement any interfaces nested within. Also, private interfaces cannot be implemented outside of their defining classes. Initially, these features may seem like they are added strictly for syntacticconsistency, but I generally find that once you know about a feature, youoften discover places where it is useful. Interfaces and factories An interface is intended to be a gateway to multiple implementations, and atypical way to produce objects that fit the interface is the Factory Methoddesign pattern. Instead of calling a constructor directly, you call a creationmethod on a factory object which produces an implementation of theinterface—this way, in theory, your code is completely isolated from the implementation of the interface, thus making it possible to transparentlyswap one implementation for another. Here’s a demonstration showing thestructure of the Factory Method:
```java
//: interfaces/Factories.java
import static net.mindview.util.Print.*;
interface Service {
void method1();
void method2();
}
interface ServiceFactory {
Service getService();
}
class Implementation1 implements Service {
Implementation1() {} // Package access
public void method1() {print("Implementation1 method1");}
public void method2() {print("Implementation1 method2");}
}
class Implementation1Factory implements ServiceFactory {
public Service getService() {
return new Implementation1();
}
}
class Implementation2 implements Service {
Implementation2() {} // Package access
public void method1() {print("Implementation2 method1");}
public void method2() {print("Implementation2 method2");}
}
class Implementation2Factory implements ServiceFactory {
public Service getService() {
return new Implementation2();
}
}
public class Factories {
public static void serviceConsumer(ServiceFactory fact) {
Service s = fact.getService();
s.method1();
s.method2();
```

<!--p262-->
Interfaces
```java
}
public static void main(String[] args) {
serviceConsumer(new Implementation1Factory());
// Implementations are completely interchangeable:
serviceConsumer(new Implementation2Factory());
}
} /* Output:
Implementation1 method1
Implementation1 method2
Implementation2 method1
Implementation2 method2
*///:~
```
Without the Factory Method, your code would somewhere have to specify theexact type of Service being created, so that it could call the appropriateconstructor. Why would you want to add this extra level of indirection? One commonreason is to create a framework. Suppose you are creating a system to playgames; for example, to play both chess and checkers on the same board:

<!--p263-->
```java
//: interfaces/Games.java
// A Game framework using Factory Methods.
import static net.mindview.util.Print.*;
interface Game { boolean move(); }
interface GameFactory { Game getGame(); }
class Checkers implements Game {
private int moves = 0;
private static final int MOVES = 3;
public boolean move() {
print("Checkers move " + moves);
return ++moves != MOVES;
}
}
class CheckersFactory implements GameFactory {
public Game getGame() { return new Checkers(); }
}
class Chess implements Game {
private int moves = 0;
private static final int MOVES = 4;
public boolean move() {
print("Chess move " + moves);
return ++moves != MOVES;
}
}
class ChessFactory implements GameFactory {
public Game getGame() { return new Chess(); }
}
public class Games {
public static void playGame(GameFactory factory) {
Game s = factory.getGame();
while(s.move())
;
}
public static void main(String[] args) {
playGame(new CheckersFactory());
playGame(new ChessFactory());
```
Interfaces
```java
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
If the Games class represents a complex piece of code, this approach allowsyou to reuse that code with different types of games. You can imagine moreelaborate games that can benefit from this pattern. In the next chapter, you’ll see a more elegant way to implement the factoriesusing anonymous inner classes. Exercise 18:(2) Create a Cycle interface, with implementations Unicycle, Bicycle and Tricycle. Create factories for each type of Cycle, and code that uses these factories. Exercise 19:(3) Create a framework using Factory Methods thatperforms both coin tossing and dice tossing. Summary It is tempting to decide that interfaces are good, and therefore you shouldalways choose interfaces over concrete classes. Of course, almost anytime youcreate a class, you could instead create an interface and a factory. Many people have fallen to this temptation, creating interfaces and factorieswherever it’s possible. The logic seems to be that you might need to use adifferent implementation, so you should always add that abstraction. It hasbecome a kind of premature design optimization. Any abstraction should be motivated by a real need. Interfaces should besomething you refactor to when necessary, rather than installing the extralevel of indirection everywhere, along with the extra complexity. That extracomplexity is significant, and if you make someone work through thatcomplexity only to realize that you’ve added interfaces "just in case" and forno compelling reason—well, if I see such a thing I begin to question all the designs that this particular person has done. An appropriate guideline is to prefer classes to interfaces. Start with classes, and if it becomes clear that interfaces are necessary, then refactor. Interfacesare a great tool, but they can easily be overused. Solutions to selected exercises can be found in the electronic document The Thinking in Java Annotated Solution Guide, available for sale from www.MindView.net.