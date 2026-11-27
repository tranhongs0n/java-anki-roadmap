# 15. Generics (printed p439-534)


<!--p461-->

<!--p462-->
Generics Ordinary classes and methods work with specific types: either primitives or class types. If you are writing code that might be used across more types, this rigidity can be overconstraining.1 One way that object-oriented languages allow generalization is through polymorphism. You can write (for example) a method that takes a base class object as an argument, and then use that method with any class derived from that base class. Now your method is a little more general and can be used in more places. The same is true within classes—anyplace you use a specific type, a base type provides more flexibility. Of course, anything but a final class2can be extended, so this flexibility is automatic much of the time. Sometimes, being constrained to a single hierarchy is too limiting. If a method argument is an interface instead of a class, the limitations are loosened to include anything that implements the interface—including classes that haven’t been created yet. This gives the client programmer the option of implementing an interface in order to conform to your class or method. So interfaces allow you to cut across class hierarchies, as long as you have the option to create a new class in order to do so. Sometimes even an interface is too restrictive. An interface still requires that your code work with that particular interface. You could write even more general code if you could say that your code works with "some unspecified type," rather than a specific interface or class. This is the concept of generics, one of the more significant changes in Java SE5. Generics implement the concept of parameterized types, which allow multiple types. The term "generic" means "pertaining or appropriate to large groups of classes." The original intent of generics in programming languages was to allow the programmer the greatest amount of expressiveness possible when writing classes or methods, by loosening the constraints on the types that those classes or methods work with. As you will see in this chapter, the Java implementation of generics is not that broad reaching—indeed, you may question whether the term "generic" is even appropriate for this feature. If you’ve never seen any kind of parameterized type mechanism before, Java generics will probably seem like a convenient addition to the language. When you create an instance of a parameterized type, casts will be taken care of for you and the type correctness will be ensured at compile time. This seems like an improvement. However, if you’ve had experience with a parameterized type mechanism, in C++, for example, you will find that you can’t do everything that you might expect when using Java generics. While using someone else’s generic type is fairly easy, when creating your own you will encounter a number of surprises. One of the things I shall try to explain is how the feature came to be like it is. This is not to say that Java generics are useless. In many cases they make code more straightforward and even elegant. But if you’re coming from a language that has implemented a more pure version of generics, you may be disappointed. In this chapter, we will examine both the strengths and the limitations of Java generics so that you can use this new feature more effectively. 1Angelika Langer’s Java Generics FAQ (see www.angelikalanger.com/GenericsFAQ/JavaGenericsFAQ.html) as well as her other writings (together with Klaus Kreft) have been invaluable during the preparation of this chapter. 2Or a class with all private constructors. Comparison with C++ The Java designers stated that much of the inspiration for the language came as a reaction to C++. Despite this, it is possible to teach Java largely without reference to C++, and I have endeavored to do so except when the comparison will give you greater depth of understanding. Generics require more comparison with C++ for two reasons. First, understanding certain aspects of C++ templates (the main inspiration for generics, including the basic syntax) will help you understand the foundations of the concept, as well as—and this is very important— the limitations of what you can do with Java generics and why. The ultimate goal is to give you a clear understanding of where the boundaries lie, because my experience is that by understanding the boundaries, you become a more powerful programmer. By knowing what you can’t do, you can make better use of what you can do (partly because you don’t waste time bumping up against walls). The second reason is that there is significant misunderstanding in the Java community about C++ templates, and this misunderstanding may further confuse you about the intent of generics. So although I will introduce a few C++ template examples in this chapter, I will keep them to a minimum. Simple generics One of the most compelling initial motivations for generics is to create container classes, which you saw in the Holding Your Objects chapter (you’ll learn more about these in the Containers in Depth chapter). A container is a place to hold objects while you’re working with them. Although this is also true of arrays, containers tend to be more flexible and have different characteristics than simple arrays. Virtually all programs require that you hold a group of objects while you use them, so containers are one of the most reusable of class libraries. Let’s look at a class that holds a single object. Of course, the class could specify the exact type of the object, like this:
```java
//: generics/Holder1.java
class Automobile {}
public class Holder1 {
private Automobile a;
public Holder1(Automobile a) { this.a = a; }
Automobile get() { return a; }
} ///:~
```
But this is not a very reusable tool, since it can’t be used to hold anything else. We would prefer not to write a new one of these for every type we encounter. Before Java SE5, we would simply make it hold an Object:

<!--p463-->
```java
//: generics/Holder2.java
public class Holder2 {
private Object a;
public Holder2(Object a) { this.a = a; }
public void set(Object a) { this.a = a; }
public Object get() { return a; }
public static void main(String[] args) {
Holder2 h2 = new Holder2(new Automobile());
Automobile a = (Automobile)h2.get();
h2.set("Not an Automobile");
String s = (String)h2.get();
h2.set(1); // Autoboxes to Integer
Integer x = (Integer)h2.get();
}
} ///:~
```
Now a Holder2 can hold anything—and in this example, a single Holder2 holds three different types of objects. There are some cases where you want a container to hold multiple types of objects, but typically you only put one type of object into a container. One of the primary motivations for generics is to specify what type of object a container holds, and to have that specification backed up by the compiler. So instead of Object, we’d like to use an unspecified type, which can be decided at a later time. To do this, you put a type parameter inside angle brackets after the class name, and then substitute an actual type when you use the class. For the "holder" class, it looks like this, where T is the type parameter:
```java
//: generics/Holder3.java
public class Holder3<T> {
private T a;
public Holder3(T a) { this.a = a; }
public void set(T a) { this.a = a; }
public T get() { return a; }
public static void main(String[] args) {
Holder3<Automobile> h3 =
new Holder3<Automobile>(new Automobile());
Automobile a = h3.get(); // No cast needed
// h3.set("Not an Automobile"); // Error
// h3.set(1); // Error
}
} ///:~
```

<!--p464-->
Now when you create a Holders, you must specify what type you want to put into it using the same angle-bracket syntax, as you can see in main( ). You are only allowed to put objects of that type (or a subtype, since the substitution principle still works with generics) into the holder. And when you get a value out, it is automatically the right type. That’s the core idea of Java generics: You tell it what type you want to use, and it takes care of the details. In general, you can treat generics as if they are any other type—they just happen to have type parameters. But as you’ll see, you can use generics just by naming them along with their type argument list. Exercise 1:(1)Use Holders with the typeinfo.pets library to show that a Holders that is specified to hold a base type can also hold a derived type. Exercise 2:(1) Create a holder class that holds three objects of the same type, along with the methods to store and fetch those objects and a constructor to initialize all three. Generics A tuple library One of the things you often want to do is return multiple objects from a method call. The return statement only allows you to specify a single object, so the answer is to create an object that holds the multiple objects that you want to return. Of course, you can write a special class every time you encounter the situation, but with generics it’s possible to solve the problem once and save yourself the effort in the future. At the same time, you are ensuring compile-time type safety. This concept is called a tuple, and it is simply a group of objects wrapped together into a single object. The recipient of the object is allowed to read the elements but not put new ones in. (This concept is also called a Data Transfer Object (or Messenger.) Tuples can typically be any length, but each object in the tuple can be of a different type. However, we want to specify the type of each object and ensure that when the recipient reads the value, they get the right type. To deal with the problem of multiple lengths, we create multiple different tuples. Here’s one that holds two objects:
```java
//: net/mindview/util/TwoTuple.java
package net.mindview.util;
public class TwoTuple<A,B> {
public final A first;
public final B second;
public TwoTuple(A a, B b) { first = a; second = b; }
public String toString() {
return "(" + first + ", " + second + ")";
}
} ///:~
```
The constructor captures the object to be stored, and toString( ) is a convenience function to display the values in a list. Note that a tuple implicitly keeps its elements in order. Upon first reading, you may think that this could violate common safety principles of Java programming. Shouldn’t first and second be private, and only accessed with methods named getFirst( ) and getSecond( )? Consider the safety that you would get in that case: Clients could still read the objects and do whatever they want with them, but they could not assign first or second to anything else. The final declaration buys you the same safety, but the above form is shorter and simpler. Another design observation is that you might want to allow a client programmer to point first or second to another object. However, it’s safer to leave it in the above form, and just force the user to create a new TwoTuple if they want one that has different elements. The longer-length tuples can be created with inheritance. You can see that adding more type parameters is a simple matter:

<!--p465-->
```java
//: net/mindview/util/ThreeTuple.java
package net.mindview.util;
public class ThreeTuple<A,B,C> extends TwoTuple<A,B> {
public final C third;
public ThreeTuple(A a, B b, C c) {
super(a, b);
third = c;
}
public String toString() {
return "(" + first + ", " + second + ", " + third +")";
}
} ///:~
//: net/mindview/util/FourTuple.java
package net.mindview.util;
public class FourTuple<A,B,C,D> extends ThreeTuple<A,B,C> {
public final D fourth;
public FourTuple(A a, B b, C c, D d) {
super(a, b, c);
fourth = d;
}
public String toString() {
return "(" + first + ", " + second + ", " +
third + ", " + fourth + ")";
}
} ///:~
//: net/mindview/util/FiveTuple.java
package net.mindview.util;
public class FiveTuple<A,B,C,D,E>
extends FourTuple<A,B,C,D> {
public final E fifth;
public FiveTuple(A a, B b, C c, D d, E e) {
super(a, b, c, d);
fifth = e;
}
public String toString() {
return "(" + first + ", " + second + ", " +
third + ", " + fourth + ", " + fifth + ")";
}
} ///:~
```
To use a tuple, you simply define the appropriate-length tuple as the return value for your function, and then create and return it in your return statement:
```java
//: generics/TupleTest.java
import net.mindview.util.*;
class Amphibian {}
class Vehicle {}
public class TupleTest {
static TwoTuple<String,Integer> f() {
// Autoboxing converts the int to Integer:
return new TwoTuple<String,Integer>("hi", 47);
}
static ThreeTuple<Amphibian,String,Integer> g() {
return new ThreeTuple<Amphibian, String, Integer>(
new Amphibian(), "hi", 47);
}
static
FourTuple<Vehicle,Amphibian,String,Integer> h() {
return
new FourTuple<Vehicle,Amphibian,String,Integer>(
new Vehicle(), new Amphibian(), "hi", 47);
}
static
FiveTuple<Vehicle,Amphibian,String,Integer,Double> k() {
return new
FiveTuple<Vehicle,Amphibian,String,Integer,Double>(
```

<!--p466-->
Generics
```java
new Vehicle(), new Amphibian(), "hi", 47, 11.1);
}
public static void main(String[] args) {
TwoTuple<String,Integer> ttsi = f();
System.out.println(ttsi);
// ttsi.first = "there"; // Compile error: final
System.out.println(g());
System.out.println(h());
System.out.println(k());
}
} /* Output: (80% match)
(hi, 47)
(Amphibian@1f6a7b9, hi, 47)
(Vehicle@35ce36, Amphibian@757aef, hi, 47)
(Vehicle@9cab16, Amphibian@1a46e30, hi, 47, 11.1)
*///:~
```
Because of generics, you can easily create any tuple to return any group of types, just by writing the expression. You can see how the final specification on the public fields prevents them from being reassigned after construction, in the failure of the statement ttsi.first = "there". The new expressions are a little verbose. Later in this chapter you’ll see how to simplify them using generic methods. Exercise 3 :(1) Create and test a SixTuple generic. Exercise 4:(3) "Generify" innerclasses/Sequence.java. A stack class Let’s look at something slightly more complicated: the traditional pushdown stack. In the Holding Your Objects chapter, you saw this implemented using a LinkedList as the net.mindview.util.Stack class (page 412). In that example, you can see that a LinkedList already has the necessary methods to create a stack. The Stack was constructed by composing one generic class (Stack<T>) with another generic class (LinkedList<T>). In that example, notice that (with a few exceptions that we shall look at later) a generic type is just another type. Instead of using LinkedList, we can implement our own internal linked storage mechanism.

<!--p467-->
```java
//: generics/LinkedStack.java
// A stack implemented with an internal linked structure.
public class LinkedStack<T> {
private static class Node<U> {
U item;
Node<U> next;
Node() { item = null; next = null; }
Node(U item, Node<U> next) {
this.item = item;
this.next = next;
}
boolean end() { return item == null && next == null; }
}
private Node<T> top = new Node<T>(); // End sentinel
public void push(T item) {
top = new Node<T>(item, top);
}
public T pop() {
T result = top.item;
if(!top.end())
top = top.next;
return result;
}
public static void main(String[] args) {
LinkedStack<String> lss = new LinkedStack<String>();
for(String s : "Phasers on stun!".split(" "))
lss.push(s);
String s;
while((s = lss.pop()) != null)
System.out.println(s);
}
} /* Output:
stun!
on
Phasers
*///:~
```
The inner class Node is also a generic, and has its own type parameter. This example makes use of an end sentinel to determine when the stack is empty. The end sentinel is created when the LinkedStack is constructed, and each time you call push( ) a new Node<T> is created and linked to the previous Node<T>. When you call pop( ), you always return the top.item, and then you discard the current Node<T> and move to the next one— except when you hit the end sentinel, in which case you don’t move. That way, if the client keeps calling pop( ), they keep getting null back to indicate that the stack is empty. Exercise 5:(2) Remove the type parameter on the Node class and modify the rest of the code in LinkedStack.java to show that an inner class has access to the generic type parameters of its outer class.
## RandomList
For another example of a holder, suppose you’d like a special type of list that randomly selects one of its elements each time you call select( ). When doing this you want to build a tool that works with all objects, so you use generics:
```java
//: generics/RandomList.java
import java.util.*;
public class RandomList<T> {
private ArrayList<T> storage = new ArrayList<T>();
private Random rand = new Random(47);
public void add(T item) { storage.add(item); }
public T select() {
return storage.get(rand.nextInt(storage.size()));
}
public static void main(String[] args) {
RandomList<String> rs = new RandomList<String>();
for(String s: ("The quick brown fox jumped over " +
"the lazy brown dog").split(" "))
rs.add(s);
for(int i = 0; i < 11; i++)
System.out.print(rs.select() + " ");
}
} /* Output:
```

<!--p468-->
Generics
```java
brown over fox quick quick dog brown The brown lazy brown
*///:~
```
Exercise 6:(1)Use RandomList with two more types in addition to the one shown in main( ). Generic interfaces Generics also work with interfaces. For example, a generator is a class that creates objects. It’s actually a specialization of the Factory Method design pattern, but when you ask a generator for new object, you don’t pass it any arguments, whereas you typically do pass arguments to a Factory Method. The generator knows how to create new objects without any extra information. Typically, a generator just defines one method, the method that produces new objects. Here, we’ll call it next( ), and include it in the standard utilities:
```java
//: net/mindview/util/Generator.java
// A generic interface.
package net.mindview.util;
public interface Generator<T> { T next(); } ///:~
```
The return type of next( ) is parameterized to T. As you can see, using generics with interfaces is no different than using generics with classes. To demonstrate the implementation of a Generator, we’ll need some classes. Here’s a coffee hierarchy:

<!--p469-->
```java
//: generics/coffee/Coffee.java
package generics.coffee;
public class Coffee {
private static long counter = 0;
private final long id = counter++;
public String toString() {
return getClass().getSimpleName() + " " + id;
}
} ///:~
//: generics/coffee/Latte.java
package generics.coffee;
public class Latte extends Coffee {} ///:~
//: generics/coffee/Mocha.java
package generics.coffee;
public class Mocha extends Coffee {} ///:~
//: generics/coffee/Cappuccino.java
package generics.coffee;
public class Cappuccino extends Coffee {} ///:~
//: generics/coffee/Americano.java
package generics.coffee;
public class Americano extends Coffee {} ///:~
//: generics/coffee/Breve.java
package generics.coffee;
public class Breve extends Coffee {} ///:~
```
Now we can implement a Generator < Coffee > that produces random different types of Coffee objects:
```java
//: generics/coffee/CoffeeGenerator.java
// Generate different types of Coffee:
package generics.coffee;
import java.util.*;
import net.mindview.util.*;
public class CoffeeGenerator
implements Generator<Coffee>, Iterable<Coffee> {
private Class[] types = { Latte.class, Mocha.class,
Cappuccino.class, Americano.class, Breve.class, };
private static Random rand = new Random(47);
public CoffeeGenerator() {}
// For iteration:
private int size = 0;
public CoffeeGenerator(int sz) { size = sz; }
public Coffee next() {
try {
return (Coffee)
types[rand.nextInt(types.length)].newInstance();
// Report programmer errors at run time:
} catch(Exception e) {
throw new RuntimeException(e);
}
}
class CoffeeIterator implements Iterator<Coffee> {
int count = size;
public boolean hasNext() { return count > 0; }
public Coffee next() {
count--;
return CoffeeGenerator.this.next();
}
public void remove() { // Not implemented
throw new UnsupportedOperationException();
}
};
public Iterator<Coffee> iterator() {
return new CoffeeIterator();
}
public static void main(String[] args) {
CoffeeGenerator gen = new CoffeeGenerator();
for(int i = 0; i < 5; i++)
System.out.println(gen.next());
for(Coffee c : new CoffeeGenerator(5))
System.out.println(c);
}
} /* Output:
Americano 0
Latte 1
Americano 2
Mocha 3
Mocha 4
Breve 5
Americano 6
Latte 7
Cappuccino 8
Cappuccino 9
*///:~
```

<!--p470-->
Generics The parameterized Generator interface ensures that next( ) returns the parameter type. CoffeeGenerator also implements the Iterable interface, so it can be used in a foreach statement. However, it requires an "end sentinel" to know when to stop, and this is produced using the second constructor. Here’s a second implementation of Generator<T>, this time to produce Fibonacci numbers:
```java
//: generics/Fibonacci.java
// Generate a Fibonacci sequence.
import net.mindview.util.*;
public class Fibonacci implements Generator<Integer> {
private int count = 0;
public Integer next() { return fib(count++); }
private int fib(int n) {
if(n < 2) return 1;
return fib(n-2) + fib(n-1);
}
public static void main(String[] args) {
Fibonacci gen = new Fibonacci();
for(int i = 0; i < 18; i++)
System.out.print(gen.next() + " ");
}
} /* Output:
1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584
*///:~
```
Although we are working with ints both inside and outside the class, the type parameter is Integer. This brings up one of the limitations of Java generics: You cannot use primitives as type parameters. However, Java SE5 conveniently added autoboxing and autounboxing to convert from primitive types to wrapper types and back. You can see the effect here because ints are seamlessly used and produced by the class. We can go one step further and make an Iterable Fibonacci generator. One option is to reimplement the class and add the Iterable interface, but you don’t always have control of the original code, and you don’t want to rewrite when you don’t have to. Instead, we can create an adapter to produce the desired interface—this design pattern was introduced earlier in the book. Adapters can be implemented in multiple ways. For example, you could use inheritance to generate the adapted class:

<!--p471-->
```java
//: generics/IterableFibonacci.java
// Adapt the Fibonacci class to make it Iterable.
import java.util.*;
public class IterableFibonacci
extends Fibonacci implements Iterable<Integer> {
private int n;
public IterableFibonacci(int count) { n = count; }
public Iterator<Integer> iterator() {
return new Iterator<Integer>() {
public boolean hasNext() { return n > 0; }
public Integer next() {
n--;
return IterableFibonacci.this.next();
}
public void remove() { // Not implemented
throw new UnsupportedOperationException();
}
};
}
public static void main(String[] args) {
for(int i : new IterableFibonacci(18))
System.out.print(i + " ");
}
} /* Output:
1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584
*///:~
```
To use IterableFibonacci in a foreach statement, you give the constructor a boundary so that hasNext( ) can know when to return false. Exercise 7:(2) Use composition instead of inheritance to adapt Fibonacci to make it Iterable. Exercise 8:(2) Following the form of the Coffee example, create a hierarchy of StoryCharacters from your favorite movie, dividing them into GoodGuys and BadGuys. Create a generator for StoryCharacters, following the form of CoffeeGenerator. Generic methods So far we’ve looked at parameterizing entire classes. You can also parameterize methods within a class. The class itself may or may not be generic—this is independent of whether you have a generic method. A generic method allows the method to vary independently of the class. As a guideline, you should use generic methods "whenever you can." That is, if it’s possible to make a method generic rather than the entire class, it’s probably going to be clearer to do so. In addition, if a method is static, it has no access to the generic type parameters of the class, so if it needs to use genericity it must be a generic method. To define a generic method, you simply place a generic parameter list before the return value, like this:
```java
//: generics/GenericMethods.java
public class GenericMethods {
public <T> void f(T x) {
System.out.println(x.getClass().getName());
}
public static void main(String[] args) {
GenericMethods gm = new GenericMethods();
gm.f("");
gm.f(1);
gm.f(1.0);
gm.f(1.0F);
gm.f(‘c’);
gm.f(gm);
}
} /* Output:
java.lang.String
java.lang.Integer
java.lang.Double
java.lang.Float
java.lang.Character
GenericMethods
```

<!--p472-->
Generics
```java
*///:~
```
The class GenericMethods is not parameterized, although both a class and its methods may be parameterized at the same time. But in this case, only the method f( ) has a type parameter, indicated by the parameter list before the method’s return type. Notice that with a generic class, you must specify the type parameters when you instantiate the class. But with a generic method, you don’t usually have to specify the parameter types, because the compiler can figure that out for you. This is called type argument inference. So calls to f( ) look like normal method calls, and it appears that f( ) has been infinitely overloaded. It will even take an argument of the type GenericMethods. For the calls to f( ) that use primitive types, autoboxing comes into play, automatically wrapping the primitive types in their associated objects. In fact, generic methods and autoboxing can eliminate some code that previously required hand conversion. Exercise 9:(1) Modify GenericMethods.java so that f( ) accepts three arguments, all of which are of a different parameterized type. Exercise 10:(1) Modify the previous exercise so that one of f( )’s arguments is non- parameterized. Leveraging type argument inference One of the complaints about generics is that it adds even more text to your code. Consider holding/MapOfList.java from the Holding Your Objects chapter. The creation of the Map of List looks like this:
```java
Map<Person, List<? extends Pet>> petPeople =
new HashMap<Person, List<? extends Pet>>();
```
(This use of extends and the question marks will be explained later in this chapter.) It appears that you are repeating yourself, and that the compiler should figure out one of the generic argument lists from the other. Alas, it cannot, but type argument inference in a generic method can produce some simplification. For example, we can create a utility containing various static methods, which produces the most commonly used implementations of the various containers:

<!--p473-->
```java
//: net/mindview/util/New.java
// Utilities to simplify generic container creation
// by using type argument inference.
package net.mindview.util;
import java.util.*;
public class New {
public static <K,V> Map<K,V> map() {
return new HashMap<K,V>();
}
public static <T> List<T> list() {
return new ArrayList<T>();
}
public static <T> LinkedList<T> lList() {
return new LinkedList<T>();
}
public static <T> Set<T> set() {
return new HashSet<T>();
}
public static <T> Queue<T> queue() {
return new LinkedList<T>();
}
// Examples:
public static void main(String[] args) {
Map<String, List<String>> sls = New.map();
List<String> ls = New.list();
LinkedList<String> lls = New.lList();
Set<String> ss = New.set();
Queue<String> qs = New.queue();
}
} ///:~
```
In main( ) you can see examples of how this is used—type argument inference eliminates the need to repeat the generic parameter list. This can be applied to holding/MapOfList.java:
```java
//: generics/SimplerPets.java
import typeinfo.pets.*;
import java.util.*;
import net.mindview.util.*;
public class SimplerPets {
public static void main(String[] args) {
Map<Person, List<? extends Pet>> petPeople = New.map();
// Rest of the code is the same...
}
} ///:~
```
Although this is an interesting example of type argument inference, it’s difficult to say how much it actually buys you. The person reading the code is required to parse and understand this additional library and its implications, so it might be just as productive to leave the original (admittedly repetitious) definition in place—ironically, for simplicity. However, if the standard Java library were to add something like the New.java utility above, it would make sense to use it. Type inference doesn’t work for anything other than assignment. If you pass the result of a method call such as New.map( ) as an argument to another method, the compiler will not try to perform type inference. Instead it will treat the method call as though the return value is assigned to a variable of type Object. Here’s an example that fails:
```java
//: generics/LimitsOfInference.java
import typeinfo.pets.*;
import java.util.*;
public class LimitsOfInference {
static void
f(Map<Person, List<? extends Pet>> petPeople) {}
public static void main(String[] args) {
// f(New.map()); // Does not compile
}
} ///:~
```

<!--p474-->
Exercise 11:(1) Test New.java by creating your own classes and ensuring that New will work properly with them. Generics Explicit type specification It is possible to explicitly specify the type in a generic method, although the syntax is rarely needed. To do so, you place the type in angle brackets after the dot and immediately preceding the method name. When calling a method from within the same class, you must use this before the dot, and when working with static methods, you must use the class name before the dot. The problem shown in LimitsOflnference.java can be solved using this syntax:
```java
//: generics/ExplicitTypeSpecification.java
import typeinfo.pets.*;
import java.util.*;
import net.mindview.util.*;
public class ExplicitTypeSpecification {
static void f(Map<Person, List<Pet>> petPeople) {}
public static void main(String[] args) {
f(New.<Person, List<Pet>>map());
}
} ///:~
```
Of course, this eliminates the benefit of using the New class to reduce the amount of typing, but the extra syntax is only required when you are not writing an assignment statement. Exercise 12:(1) Repeat the previous exercise using explicit type specification. Varargs and generic methods Generic methods and variable argument lists coexist nicely:
```java
//: generics/GenericVarargs.java
import java.util.*;
public class GenericVarargs {
public static <T> List<T> makeList(T... args) {
List<T> result = new ArrayList<T>();
for(T item : args)
result.add(item);
return result;
}
public static void main(String[] args) {
List<String> ls = makeList("A");
System.out.println(ls);
ls = makeList("A", "B", "C");
System.out.println(ls);
ls = makeList("ABCDEFFHIJKLMNOPQRSTUVWXYZ".split(""));
System.out.println(ls);
}
} /* Output:
[A]
[A, B, C]
[, A, B, C, D, E, F, F, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W,
X, Y, Z]
*///:~
```

<!--p475-->
The makeList( ) method shown here produces the same functionality as the standard library’s java.util.Arrays.asList( ) method. A generic method to use with
## Generators
It is convenient to use a generator to fill a Collection, and it makes sense to "generify" this operation:
```java
//: generics/Generators.java
// A utility to use with Generators.
import generics.coffee.*;
import java.util.*;
import net.mindview.util.*;
public class Generators {
public static <T> Collection<T>
fill(Collection<T> coll, Generator<T> gen, int n) {
for(int i = 0; i < n; i++)
coll.add(gen.next());
return coll;
}
public static void main(String[] args) {
Collection<Coffee> coffee = fill(
new ArrayList<Coffee>(), new CoffeeGenerator(), 4);
for(Coffee c : coffee)
System.out.println(c);
Collection<Integer> fnumbers = fill(
new ArrayList<Integer>(), new Fibonacci(), 12);
for(int i : fnumbers)
System.out.print(i + ", ");
}
} /* Output:
Americano 0
Latte 1
Americano 2
Mocha 3
1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144,
*///:~
```
Notice how the generic method fill( ) can be transparently applied to both Coffee and Integer containers and generators. Exercise 13:(4) Overload the fill( ) method so that the arguments and return types are the specific subtypes of Collection: List, Queue and Set. This way, you don’t lose the type of container. Can you overload to distinguish between List and LinkedList?
## A general-purpose Generator
Here’s a class that produces a Generator for any class that has a default constructor. To reduce typing, it also includes a generic method to produce a BasicGenerator:
```java
//: net/mindview/util/BasicGenerator.java
// Automatically create a Generator, given a class
// with a default (no-arg) constructor.
package net.mindview.util;
public class BasicGenerator<T> implements Generator<T> {
private Class<T> type;
public BasicGenerator(Class<T> type){ this.type = type; }
public T next() {
```

<!--p476-->
Generics
```java
try {
// Assumes type is a public class:
return type.newInstance();
} catch(Exception e) {
throw new RuntimeException(e);
}
}
// Produce a Default generator given a type token:
public static <T> Generator<T> create(Class<T> type) {
return new BasicGenerator<T>(type);
}
} ///:~
```
This class provides a basic implementation that will produce objects of a class that (1) is public (because BasicGenerator is in a separate package, the class in question must have public and not just package access) and (2) has a default constructor (one that takes no arguments). To create one of these BasicGenerator objects, you call the create( ) method and pass it the type token for the type you want generated. The generic create( ) method allows you to say BasicGenerator.create(MyType.class) instead of the more awkward new BasicGenerator<MyType>(MyType.class). For example, here’s a simple class that has a default constructor:
```java
//: generics/CountedObject.java
public class CountedObject {
private static long counter = 0;
private final long id = counter++;
public long id() { return id; }
public String toString() { return "CountedObject " + id;}
} ///:~
```
The CountedObject class keeps track of how many instances of itself have been created, and reports these in its toString( ). Using BasicGenerator, you can easily create a Generator for CountedObject:
```java
//: generics/BasicGeneratorDemo.java
import net.mindview.util.*;
public class BasicGeneratorDemo {
public static void main(String[] args) {
Generator<CountedObject> gen =
BasicGenerator.create(CountedObject.class);
for(int i = 0; i < 5; i++)
System.out.println(gen.next());
}
} /* Output:
CountedObject 0
CountedObject 1
CountedObject 2
CountedObject 3
CountedObject 4
*///:~
```

<!--p477-->
You can see how the generic method reduces the amount of typing necessary to produce the Generator object. Java generics force you to pass in the Class object anyway, so you might as well use it for type inference in the create( ) method. Exercise 14:(1) Modify BasicGeneratorDemo.java to use the explicit form of creation for the Generator (that is, use the explicit constructor instead of the generic create( ) method). Simplifying tuple use Type argument inference, together with static imports, allows the tuples we saw earlier to be rewritten into a more general-purpose library. Here, tuples can be created using an overloaded static method:
```java
//: net/mindview/util/Tuple.java
// Tuple library using type argument inference.
package net.mindview.util;
public class Tuple {
public static <A,B> TwoTuple<A,B> tuple(A a, B b) {
return new TwoTuple<A,B>(a, b);
}
public static <A,B,C> ThreeTuple<A,B,C>
tuple(A a, B b, C c) {
return new ThreeTuple<A,B,C>(a, b, c);
}
public static <A,B,C,D> FourTuple<A,B,C,D>
tuple(A a, B b, C c, D d) {
return new FourTuple<A,B,C,D>(a, b, c, d);
}
public static <A,B,C,D,E>
FiveTuple<A,B,C,D,E> tuple(A a, B b, C c, D d, E e) {
return new FiveTuple<A,B,C,D,E>(a, b, c, d, e);
}
} ///:~
```
Here’s a modification of TupleTest.java to test Tuple.java:
```java
//: generics/TupleTest2.java
import net.mindview.util.*;
import static net.mindview.util.Tuple.*;
public class TupleTest2 {
static TwoTuple<String,Integer> f() {
return tuple("hi", 47);
}
static TwoTuple f2() { return tuple("hi", 47); }
static ThreeTuple<Amphibian,String,Integer> g() {
return tuple(new Amphibian(), "hi", 47);
}
static
FourTuple<Vehicle,Amphibian,String,Integer> h() {
return tuple(new Vehicle(), new Amphibian(), "hi", 47);
}
static
FiveTuple<Vehicle,Amphibian,String,Integer,Double> k() {
return tuple(new Vehicle(), new Amphibian(),
"hi", 47, 11.1);
}
public static void main(String[] args) {
TwoTuple<String,Integer> ttsi = f();
System.out.println(ttsi);
System.out.println(f2());
System.out.println(g());
```

<!--p478-->
Generics
```java
System.out.println(h());
System.out.println(k());
}
} /* Output: (80% match)
(hi, 47)
(hi, 47)
(Amphibian@7d772e, hi, 47)
(Vehicle@757aef, Amphibian@d9f9c3, hi, 47)
(Vehicle@1a46e30, Amphibian@3e25a5, hi, 47, 11.1)
*///:~
```
Notice that f( ) returns a parameterized TwoTuple object, while f2( ) returns an unparameterized TwoTuple object. The compiler doesn’t warn about f2( ) in this case because the return value is not being used in a parameterized fashion; in a sense, it is being "upcast" to an unparameterized TwoTuple. However, if you were to try to capture the result of f2( ) into a parameterized TwoTuple, the compiler would issue a warning. Exercise 15:(1) Verify the previous statement. Exercise 16: (2)Add a SixTuple to Tuple.java, and test it in TupleTest2 .j ava.
## A Set utility
For another example of the use of generic methods, consider the mathematical relationships that can be expressed using Sets. These can be conveniently defined as generic methods, to be used with all different types:
```java
//: net/mindview/util/Sets.java
package net.mindview.util;
import java.util.*;
public class Sets {
public static <T> Set<T> union(Set<T> a, Set<T> b) {
Set<T> result = new HashSet<T>(a);
result.addAll(b);
return result;
}
public static <T>
Set<T> intersection(Set<T> a, Set<T> b) {
Set<T> result = new HashSet<T>(a);
result.retainAll(b);
return result;
}
// Subtract subset from superset:
public static <T> Set<T>
difference(Set<T> superset, Set<T> subset) {
Set<T> result = new HashSet<T>(superset);
result.removeAll(subset);
return result;
}
// Reflexive--everything not in the intersection:
public static <T> Set<T> complement(Set<T> a, Set<T> b) {
return difference(union(a, b), intersection(a, b));
}
} ///:~
```

<!--p479-->
The first three methods duplicate the first argument by copying its references into a new HashSet object, so the argument Sets are not directly modified. The return value is thus a new Set object. The four methods represent mathematical set operations: union( ) returns a Set containing the combination of the two arguments, intersection( ) returns a Set containing the common elements between the two arguments, difference( ) performs a subtraction of the subset elements from the superset, and complement( ) returns a Set of all the elements that are not in the intersection. To create a simple example showing the effects of these methods, here’s an enum containing different names of watercolors:
```java
//: generics/watercolors/Watercolors.java
package generics.watercolors;
public enum Watercolors {
ZINC, LEMON_YELLOW, MEDIUM_YELLOW, DEEP_YELLOW, ORANGE,
BRILLIANT_RED, CRIMSON, MAGENTA, ROSE_MADDER, VIOLET,
CERULEAN_BLUE_HUE, PHTHALO_BLUE, ULTRAMARINE,
COBALT_BLUE_HUE, PERMANENT_GREEN, VIRIDIAN_HUE,
SAP_GREEN, YELLOW_OCHRE, BURNT_SIENNA, RAW_UMBER,
BURNT_UMBER, PAYNES_GRAY, IVORY_BLACK
} ///:~
```
For convenience (so that all the names don’t have to be qualified), this is imported statically into the following example. This example uses the EnumSet, which is a Java SE5 tool for easy creation of Sets from enums. (You’ll learn more about EnumSet in the Enumerated Types chapter.) Here, the static method EnumSet.range( ) is given the first and last elements of the range to create in the resulting Set:
```java
//: generics/WatercolorSets.java
import generics.watercolors.*;
import java.util.*;
import static net.mindview.util.Print.*;
import static net.mindview.util.Sets.*;
import static generics.watercolors.Watercolors.*;
public class WatercolorSets {
public static void main(String[] args) {
Set<Watercolors> set1 =
EnumSet.range(BRILLIANT_RED, VIRIDIAN_HUE);
Set<Watercolors> set2 =
EnumSet.range(CERULEAN_BLUE_HUE, BURNT_UMBER);
print("set1: " + set1);
print("set2: " + set2);
print("union(set1, set2): " + union(set1, set2));
Set<Watercolors> subset = intersection(set1, set2);
print("intersection(set1, set2): " + subset);
print("difference(set1, subset): " +
difference(set1, subset));
print("difference(set2, subset): " +
difference(set2, subset));
print("complement(set1, set2): " +
complement(set1, set2));
}
} /* Output: (Sample)
set1: [BRILLIANT_RED, CRIMSON, MAGENTA, ROSE_MADDER, VIOLET,
CERULEAN_BLUE_HUE, PHTHALO_BLUE, ULTRAMARINE, COBALT_BLUE_HUE,
PERMANENT_GREEN, VIRIDIAN_HUE]
set2: [CERULEAN_BLUE_HUE, PHTHALO_BLUE, ULTRAMARINE, COBALT_BLUE_HUE,
PERMANENT_GREEN, VIRIDIAN_HUE, SAP_GREEN, YELLOW_OCHRE, BURNT_SIENNA,
RAW_UMBER, BURNT_UMBER]
union(set1, set2): [SAP_GREEN, ROSE_MADDER, YELLOW_OCHRE,
PERMANENT_GREEN, BURNT_UMBER, COBALT_BLUE_HUE, VIOLET, BRILLIANT_RED,
RAW_UMBER, ULTRAMARINE, BURNT_SIENNA, CRIMSON, CERULEAN_BLUE_HUE,
PHTHALO_BLUE, MAGENTA, VIRIDIAN_HUE]
```

<!--p480-->
Generics
```java
intersection(set1, set2): [ULTRAMARINE, PERMANENT_GREEN,
COBALT_BLUE_HUE, PHTHALO_BLUE, CERULEAN_BLUE_HUE, VIRIDIAN_HUE]
difference(set1, subset): [ROSE_MADDER, CRIMSON, VIOLET, MAGENTA,
BRILLIANT_RED]
difference(set2, subset): [RAW_UMBER, SAP_GREEN, YELLOW_OCHRE,
BURNT_SIENNA, BURNT_UMBER]
complement(set1, set2): [SAP_GREEN, ROSE_MADDER, YELLOW_OCHRE,
BURNT_UMBER, VIOLET, BRILLIANT_RED, RAW_UMBER, BURNT_SIENNA, CRIMSON,
MAGENTA]
*///:~
```
You can see the results of each operation from the output. The following example uses Sets.difference( ) to show the method differences between various Collection and Map classes in java.util:

<!--p481-->
```java
//: net/mindview/util/ContainerMethodDifferences.java
package net.mindview.util;
import java.lang.reflect.*;
import java.util.*;
public class ContainerMethodDifferences {
static Set<String> methodSet(Class<?> type) {
Set<String> result = new TreeSet<String>();
for(Method m : type.getMethods())
result.add(m.getName());
return result;
}
static void interfaces(Class<?> type) {
System.out.print("Interfaces in " +
type.getSimpleName() + ": ");
List<String> result = new ArrayList<String>();
for(Class<?> c : type.getInterfaces())
result.add(c.getSimpleName());
System.out.println(result);
}
static Set<String> object = methodSet(Object.class);
static { object.add("clone"); }
static void
difference(Class<?> superset, Class<?> subset) {
System.out.print(superset.getSimpleName() +
" extends " + subset.getSimpleName() + ", adds: ");
Set<String> comp = Sets.difference(
methodSet(superset), methodSet(subset));
comp.removeAll(object); // Don’t show ‘Object’ methods
System.out.println(comp);
interfaces(superset);
}
public static void main(String[] args) {
System.out.println("Collection: " +
methodSet(Collection.class));
interfaces(Collection.class);
difference(Set.class, Collection.class);
difference(HashSet.class, Set.class);
difference(LinkedHashSet.class, HashSet.class);
difference(TreeSet.class, Set.class);
difference(List.class, Collection.class);
difference(ArrayList.class, List.class);
difference(LinkedList.class, List.class);
difference(Queue.class, Collection.class);
difference(PriorityQueue.class, Queue.class);
System.out.println("Map: " + methodSet(Map.class));
difference(HashMap.class, Map.class);
difference(LinkedHashMap.class, HashMap.class);
difference(SortedMap.class, Map.class);
difference(TreeMap.class, Map.class);
}
} ///:~
```
The output of this program was used in the "Summary" section of the Holding Your Objects chapter. Exercise 17:(4) Study the JDK documentation for EnumSet. You’ll see that there’s a clone( ) method defined. However, you cannot clone( ) from the reference to the Set interface passed in Sets.java. Can you modify Sets.java to handle both the general case of a Set interface as shown, and the special case of an EnumSet, using clone( ) instead of creating a new HashSet? Anonymous inner classes Generics can also be used with inner classes and anonymous inner classes. Here’s an example that implements the Generator interface using anonymous inner classes:
```java
//: generics/BankTeller.java
// A very simple bank teller simulation.
import java.util.*;
import net.mindview.util.*;
class Customer {
private static long counter = 1;
private final long id = counter++;
private Customer() {}
public String toString() { return "Customer " + id; }
// A method to produce Generator objects:
public static Generator<Customer> generator() {
return new Generator<Customer>() {
public Customer next() { return new Customer(); }
};
}
}
class Teller {
private static long counter = 1;
private final long id = counter++;
private Teller() {}
public String toString() { return "Teller " + id; }
// A single Generator object:
public static Generator<Teller> generator =
new Generator<Teller>() {
public Teller next() { return new Teller(); }
};
}
public class BankTeller {
public static void serve(Teller t, Customer c) {
System.out.println(t + " serves " + c);
}
public static void main(String[] args) {
Random rand = new Random(47);
Queue<Customer> line = new LinkedList<Customer>();
Generators.fill(line, Customer.generator(), 15);
List<Teller> tellers = new ArrayList<Teller>();
Generators.fill(tellers, Teller.generator, 4);
```

<!--p482-->
Generics
```java
for(Customer c : line)
serve(tellers.get(rand.nextInt(tellers.size())), c);
}
} /* Output:
Teller 3 serves Customer 1
Teller 2 serves Customer 2
Teller 3 serves Customer 3
Teller 1 serves Customer 4
Teller 1 serves Customer 5
Teller 3 serves Customer 6
Teller 1 serves Customer 7
Teller 2 serves Customer 8
Teller 3 serves Customer 9
Teller 3 serves Customer 10
Teller 2 serves Customer 11
Teller 4 serves Customer 12
Teller 2 serves Customer 13
Teller 1 serves Customer 14
Teller 1 serves Customer 15
*///:~
```
Both Customer and Teller have private constructors, thereby forcing you to use Generator objects. Customer has a generator( ) method that produces a new Generator<Customer> object each time you call it. You may not need multiple Generator objects, and Teller creates a single public generator object. You can see both of these approaches used in the fill( ) methods in main( ). Since both the generator( ) method in Customer and the Generator object in Teller are static, they cannot be part of an interface, so there is no way to "generify" this particular idiom. Despite that, it works reasonably well with the fill( ) method. We’ll look at other versions of this queuing problem in the Concurrency chapter. Exercise 18:(3) Following the form of BankTeller.java, create an example where BigFish eat LittleFish in the Ocean. Building complex models An important benefit of generics is the ability to simply and safely create complex models. For example, we can easily create a List of tuples:

<!--p483-->
```java
//: generics/TupleList.java
// Combining generic types to make complex generic types.
import java.util.*;
import net.mindview.util.*;
public class TupleList<A,B,C,D>
extends ArrayList<FourTuple<A,B,C,D>> {
public static void main(String[] args) {
TupleList<Vehicle, Amphibian, String, Integer> tl =
new TupleList<Vehicle, Amphibian, String, Integer>();
tl.add(TupleTest.h());
tl.add(TupleTest.h());
for(FourTuple<Vehicle,Amphibian,String,Integer> i: tl)
System.out.println(i);
}
} /* Output: (75% match)
(Vehicle@11b86e7, Amphibian@35ce36, hi, 47)
(Vehicle@757aef, Amphibian@d9f9c3, hi, 47)
*///:~
```
Although it gets somewhat verbose (especially the creation of the iterator), you end up with a fairly powerful data structure without too much code. Here’s another example showing how straightforward it is to build complex models using generic types. Even though each class is created as a building block, the total has many parts. In this case, the model is a retail store with aisles, shelves and products:
```java
//: generics/Store.java
// Building up a complex model using generic containers.
import java.util.*;
import net.mindview.util.*;
class Product {
private final int id;
private String description;
private double price;
public Product(int IDnumber, String descr, double price){
id = IDnumber;
description = descr;
this.price = price;
System.out.println(toString());
}
public String toString() {
return id + ": " + description + ", price: $" + price;
}
public void priceChange(double change) {
price += change;
}
public static Generator<Product> generator =
new Generator<Product>() {
private Random rand = new Random(47);
public Product next() {
return new Product(rand.nextInt(1000), "Test",
Math.round(rand.nextDouble() * 1000.0) + 0.99);
}
};
}
class Shelf extends ArrayList<Product> {
public Shelf(int nProducts) {
Generators.fill(this, Product.generator, nProducts);
}
}
class Aisle extends ArrayList<Shelf> {
public Aisle(int nShelves, int nProducts) {
for(int i = 0; i < nShelves; i++)
add(new Shelf(nProducts));
}
}
class CheckoutStand {}
class Office {}
public class Store extends ArrayList<Aisle> {
private ArrayList<CheckoutStand> checkouts =
new ArrayList<CheckoutStand>();
private Office office = new Office();
public Store(int nAisles, int nShelves, int nProducts) {
for(int i = 0; i < nAisles; i++)
```

<!--p484-->
Generics
```java
add(new Aisle(nShelves, nProducts));
}
public String toString() {
StringBuilder result = new StringBuilder();
for(Aisle a : this)
for(Shelf s : a)
for(Product p : s) {
result.append(p);
result.append("\n");
}
return result.toString();
}
public static void main(String[] args) {
System.out.println(new Store(14, 5, 10));
}
} /* Output:
258: Test, price: $400.99
861: Test, price: $160.99
868: Test, price: $417.99
207: Test, price: $268.99
551: Test, price: $114.99
278: Test, price: $804.99
520: Test, price: $554.99
140: Test, price: $530.99
...
*///:~
```
As you can see in Store.toString( ), the result is many layers of containers that are nonetheless type-safe and manageable. What’s impressive is that it is not intellectually prohibitive to assemble such a model. Exercise 19:(2) Following the form of Store.java, build a model of a containerized cargo ship. The mystery of erasure As you begin to delve more deeply into generics, there are a number of things that won’t initially make sense. For example, although you can say ArrayList.class, you cannot say ArrayList<Integer>.class. And consider the following:
```java
//: generics/ErasedTypeEquivalence.java
import java.util.*;
public class ErasedTypeEquivalence {
public static void main(String[] args) {
Class c1 = new ArrayList<String>().getClass();
Class c2 = new ArrayList<Integer>().getClass();
System.out.println(c1 == c2);
}
} /* Output:
true
*///:~
```

<!--p485-->
Array List < String > and Array List < Integer > could easily be argued to be distinct types. Different types behave differently, and if you try, for example, to put an Integer into an Array List < String >, you get different behavior (it fails) than if you put an Integer into an ArrayList< Integer > (it succeeds). And yet the above program suggests that they are the same type. Here’s an example that adds to this puzzle:
```java
//: generics/LostInformation.java
import java.util.*;
class Frob {}
class Fnorkle {}
class Quark<Q> {}
class Particle<POSITION,MOMENTUM> {}
public class LostInformation {
public static void main(String[] args) {
List<Frob> list = new ArrayList<Frob>();
Map<Frob,Fnorkle> map = new HashMap<Frob,Fnorkle>();
Quark<Fnorkle> quark = new Quark<Fnorkle>();
Particle<Long,Double> p = new Particle<Long,Double>();
System.out.println(Arrays.toString(
list.getClass().getTypeParameters()));
System.out.println(Arrays.toString(
map.getClass().getTypeParameters()));
System.out.println(Arrays.toString(
quark.getClass().getTypeParameters()));
System.out.println(Arrays.toString(
p.getClass().getTypeParameters()));
}
} /* Output:
[E]
[K, V]
[Q]
[POSITION, MOMENTUM]
*///:~
```

<!--p486-->
According to the JDK documentation, Class.getTypeParameters( ) "returns an array of TypeVariable objects that represent the type variables declared by the generic declaration..." This seems to suggest that you might be able to find out what the parameter types are. However, as you can see from the output, all you find out is the identifiers that are used as the parameter placeholders, which is not such an interesting piece of information. The cold truth is: There’s no information about generic parameter types available inside generic code. Thus, you can know things like the identifier of the type parameter and the bounds of the generic type—you just can’t know the actual type parameter(s) used to create a particular instance. This fact, which is especially frustrating if you’re coming from C++, is the most fundamental issue that you must deal with when working with Java generics. Java generics are implemented using erasure. This means that any specific type information is erased when you use a generic. Inside the generic, the only thing that you know is that you’re using an object. So List<String> and List< Integer> are, in fact, the same type at run time. Both forms are "erased" to their raw type, List. Understanding erasure and how you must deal with it will be one of the biggest hurdles you will face when learning Java generics, and that’s what we’ll explore in this section. Generics The C++ approach Here’s a C++ example which uses templates. You’ll notice that the syntax for parameterized types is quite similar, because Java took inspiration from C++:
```java
//: generics/Templates.cpp
#include <iostream>
using namespace std;
template<class T> class Manipulator {
T obj;
public:
Manipulator(T x) { obj = x; }
void manipulate() { obj.f(); }
};
class HasF {
public:
void f() { cout << "HasF::f()" << endl; }
};
int main() {
HasF hf;
Manipulator<HasF> manipulator(hf);
manipulator.manipulate();
} /* Output:
HasF::f()
///:~
```
The Manipulator class stores an object of type T. What’s interesting is the manipulate( ) method, which calls a method f( ) on obj. How can it know that the f( ) method exists for the type parameter T? The C++ compiler checks when you instantiate the template, so at the point of instantiation of Manipulator <HasF>, it sees that HasF has a method f( ). If it were not the case, you’d get a compile-time error, and thus type safety is preserved. Writing this kind of code in C++ is straightforward because when a template is instantiated, the template code knows the type of its template parameters. Java generics are different. Here’s the translation of HasF:
```java
//: generics/HasF.java
public class HasF {
public void f() { System.out.println("HasF.f()"); }
} ///:~
```
If we take the rest of the example and translate it to Java, it won’t compile:

<!--p487-->
```java
//: generics/Manipulation.java
// {CompileTimeError} (Won’t compile)
class Manipulator<T> {
private T obj;
public Manipulator(T x) { obj = x; }
// Error: cannot find symbol: method f():
public void manipulate() { obj.f(); }
}
public class Manipulation {
public static void main(String[] args) {
HasF hf = new HasF();
Manipulator<HasF> manipulator =
new Manipulator<HasF>(hf);
manipulator.manipulate();
}
} ///:~
```
Because of erasure, the Java compiler can’t map the requirement that manipulate( ) must be able to call f( ) on obj to the fact that HasF has a method f( ). In order to call f( ), we must assist the generic class by giving it a bound that tells the compiler to only accept types that conform to that bound. This reuses the extends keyword. Because of the bound, the following compiles:
```java
//: generics/Manipulator2.java
class Manipulator2<T extends HasF> {
private T obj;
public Manipulator2(T x) { obj = x; }
public void manipulate() { obj.f(); }
} ///:~
```
The bound <T extends HasF> says that T must be of type HasF or something derived from HasF. If this is true, then it is safe to call f( ) on obj. We say that a generic type parameter erases to its first bound (it’s possible to have multiple bounds, as you shall see later). We also talk about the erasure of the type parameter. The compiler actually replaces the type parameter with its erasure, so in the above case, T erases to HasF, which is the same as replacing T with HasF in the class body. You may correctly observe that in Manipulations.Java, generics do not contribute anything. You could just as easily perform the erasure yourself and produce a class without generics:
```java
//: generics/Manipulator3.java
class Manipulator3 {
private HasF obj;
public Manipulator3(HasF x) { obj = x; }
public void manipulate() { obj.f(); }
} ///:~
```
This brings up an important point: Generics are only useful when you want to use type parameters that are more "generic" than a specific type (and all its subtypes)—that is, when you want code to work across multiple classes. As a result, the type parameters and their application in useful generic code will usually be more complex than simple class replacement. However, you can’t just say that anything of the form <T extends HasF> is therefore flawed. For example, if a class has a method that returns T, then generics are helpful, because they will then return the exact type:
```java
//: generics/ReturnGenericType.java
class ReturnGenericType<T extends HasF> {
private T obj;
public ReturnGenericType(T x) { obj = x; }
public T get() { return obj; }
} ///:~
```

<!--p488-->

<!--p489-->
You have to look at all the code and understand whether it is "complex enough" to warrant the use of generics. Generics We’ll look at bounds in more detail later in the chapter. Exercise 20:(1) Create an interface with two methods, and a class that implements that interface and adds another method. In another class, create a generic method with an argument type that is bounded by the interface, and show that the methods in the interface are callable inside this generic method. In main( ), pass an instance of the implementing class to the generic method. Migration compatibility To allay any potential confusion about erasure, you must clearly understand that it is not a language feature. It is a compromise in the implementation of Java generics, necessary because generics were not made part of the language from the beginning. This compromise will cause you pain, so you need to get used to it early and to understand why it’s there. If generics had been part of Java l.o, the feature would not have been implemented using erasure—it would have used reification to retain the type parameters as first-class entities, so you would have been able to perform type-based language and reflective operations on type parameters. You’ll see later in this chapter that erasure reduces the "genericity" of generics. Generics are still useful in Java, just not as useful as they could be, and the reason is erasure. In an erasure-based implementation, generic types are treated as secondclass types that cannot be used in some important contexts. The generic types are present only during static type checking, after which every generic type in the program is erased by replacing it with a non-generic upper bound. For example, type annotations such as List<T> are erased to List, and ordinary type variables are erased to Object unless a bound is specified. The core motivation for erasure is that it allows generified clients to be used with non- generified libraries, and vice versa. This is often called migration compatibility. In the ideal world, we would have had a single day when everything was generified at once. In reality, even if programmers are only writing generic code, they will have to deal with non-generic libraries that were written before Java SE5. The authors of those libraries may never have the incentive to generify their code, or they may just take their time in getting to it. So Java generics not only must support backwards compatibility—existing code and class files are still legal, and continue to mean what they meant before—but also must support migration compatibility, so that libraries can become generic at their own pace, and when a library does become generic, it doesn’t break code and applications that depend upon it. After deciding that this was the goal, the Java designers and the various groups working on the problem decided that erasure was the only feasible solution. Erasure enables this migration towards generics by allowing non-generic code to coexist with generic code. For example, suppose an application uses two libraries, X and Y, and Y uses library Z. With the advent of Java SE5, the creators of this application and these libraries will probably, eventually, want to migrate to generics. Each of them, however, will have different motivations and constraints as to when that migration happens. To achieve migration compatibility, each library and application must be independent of all the others regarding whether generics are used. Thus, they must not be able to detect whether other libraries are or are not using generics. Ergo, the evidence that a particular library is using generics must be "erased." Without some kind of migration path, all the libraries that had been built up over time stood the chance of being cut off from the developers that chose to move to Java generics. Libraries are arguably the part of a programming language that has the greatest productivity impact, so this was not an acceptable cost. Whether or not erasure was the best or only migration path is something that only time will tell. The problem with erasure So the primary justification for erasure is the transition process from nongenerified code to generified code, and to incorporate generics into the language without breaking existing libraries. Erasure allows existing nongeneric client code to continue to be used without change, until clients are ready to rewrite code for generics. This is a noble motivation, because it doesn’t suddenly break all existing code. The cost of erasure is significant. Generic types cannot be used in operations that explicitly refer to runtime types, such as casts, instanceof operations, and new expressions. Because all the type information about the parameters is lost, whenever you’re writing generic code you must constantly be reminding yourself that it only appears that you have type information about a parameter. So when you write a piece of code like this:
```java
class Foo<T> {
T var;
}
```
it appears that when you create an instance of Foo:
```java
Foo<Cat> f = new Foo<Cat>();
```
the code in class Foo ought to know that it is now working with a Cat. The syntax strongly suggests that the type T is being substituted everywhere throughout the class. But it isn’t, and you must remind yourself, "No, it’s just an Object,"whenever you’re writing the code for the class. In addition, erasure and migration compatibility mean that the use of generics is not enforced when you might want it to be:
```java
//: generics/ErasureAndInheritance.java
class GenericBase<T> {
private T element;
public void set(T arg) { arg = element; }
public T get() { return element; }
}
class Derived1<T> extends GenericBase<T> {}
class Derived2 extends GenericBase {} // No warning
// class Derived3 extends GenericBase<?> {}
// Strange error:
// unexpected type found : ?
// required: class or interface without bounds
public class ErasureAndInheritance {
@SuppressWarnings("unchecked")
public static void main(String[] args) {
Derived2 d2 = new Derived2();
Object obj = d2.get();
d2.set(obj); // Warning here!
}
} ///:~
```

<!--p490-->
Derived2 inherits from GenericBase with no generic parameters, and the compiler doesn’t issue a warning. The warning doesn’t occur until set( ) is called. Generics To turn off the warning, Java provides an annotation, the one that you see in the listing (this annotation was not supported in earlier releases of Java SE5):
```java
@SuppressWarnings("unchecked")
```
Notice that this is placed on the method that generates the warning, rather than the entire class. It’s best to be as "focused" as possible when you turn off a warning, so that you don’t accidentally cloak a real problem by turning off warnings too broadly. Presumably, the error produced by Derived3 means that the compiler expects a raw base class. Add to this the extra effort of managing bounds when you want to treat your type parameter as more than just an Object, and you have far more effort for much less payoff than you get in parameterized types in languages like C++, Ada or Eiffel. This is not to say that those languages in general buy you more than Java does for the majority of programming problems, but rather that their parameterized type mechanisms are more flexible and powerful than Java’s. The action at the boundaries Because of erasure, I find that the most confusing aspect of generics is the fact that you can represent things that have no meaning. For example:
```java
//: generics/ArrayMaker.java
import java.lang.reflect.*;
import java.util.*;
public class ArrayMaker<T> {
private Class<T> kind;
public ArrayMaker(Class<T> kind) { this.kind = kind; }
@SuppressWarnings("unchecked")
T[] create(int size) {
return (T[])Array.newInstance(kind, size);
}
public static void main(String[] args) {
ArrayMaker<String> stringMaker =
new ArrayMaker<String>(String.class);
String[] stringArray = stringMaker.create(9);
System.out.println(Arrays.toString(stringArray));
}
} /* Output:
[null, null, null, null, null, null, null, null, null]
*///:~
```
Even though kind is stored as Class<T>, erasure means that it is actually just being stored as a Class, with no parameter. So, when you do something with it, as in creating an array, Array.newInstance( ) doesn’t actually have the type information that’s implied in kind; so it cannot produce the specific result, which must therefore be cast, which produces a warning that you cannot satisfy. Note that using Array.newInstance( ) is the recommended approach for creating arrays in generics. If we create a container instead of an array, things are different:

<!--p491-->
```java
//: generics/ListMaker.java
import java.util.*;
public class ListMaker<T> {
List<T> create() { return new ArrayList<T>(); }
public static void main(String[] args) {
ListMaker<String> stringMaker= new ListMaker<String>();
List<String> stringList = stringMaker.create();
}
} ///:~
```
The compiler gives no warnings, even though we know (from erasure) that the <T> in new ArrayList<T>( ) inside create( ) is removed—at run time there’s no <T> inside the class, so it seems meaningless. But if you follow this idea and change the expression to new ArrayList( ), the compiler gives a warning. Is it really meaningless in this case? What if you were to put some objects in the list before returning it, like this:
```java
//: generics/FilledListMaker.java
import java.util.*;
public class FilledListMaker<T> {
List<T> create(T t, int n) {
List<T> result = new ArrayList<T>();
for(int i = 0; i < n; i++)
result.add(t);
return result;
}
public static void main(String[] args) {
FilledListMaker<String> stringMaker =
new FilledListMaker<String>();
List<String> list = stringMaker.create("Hello", 4);
System.out.println(list);
}
} /* Output:
[Hello, Hello, Hello, Hello]
*///:~
```
Even though the compiler is unable to know anything about T inside create( ), it can still ensure—at compile time—that what you put into result is of type T, so that it agrees with ArrayList<T>. Thus, even though erasure removes the information about the actual type inside a method or class, the compiler can still ensure internal consistency in the way that the type is used within the method or class. Because erasure removes type information in the body of a method, what matters at run time is the boundaries: the points where objects enter and leave a method. These are the points at which the compiler performs type checks at compile time, and inserts casting code. Consider the following nongeneric example:
```java
//: generics/SimpleHolder.java
public class SimpleHolder {
private Object obj;
public void set(Object obj) { this.obj = obj; }
public Object get() { return obj; }
public static void main(String[] args) {
SimpleHolder holder = new SimpleHolder();
holder.set("Item");
String s = (String)holder.get();
}
} ///:~
```

<!--p492-->
Generics If we decompile the result with javap -c SimpleHolder, we get (after editing):
```java
public void set(java.lang.Object);
0: aload_0
1: aload_1
2: putfield #2; //Field obj:Object;
5: return
public java.lang.Object get();
0: aload_0
1: getfield #2; //Field obj:Object;
4: areturn
public static void main(java.lang.String[]);
0: new #3; //class SimpleHolder
3: dup
4: invokespecial #4; //Method "<init>":()V
7: astore_1
8: aload_1
9: ldc #5; //String Item
11: invokevirtual #6; //Method set:(Object;)V
14: aload_1
15: invokevirtual #7; //Method get:()Object;
18: checkcast #8; //class java/lang/String
21: astore_2
22: return
```
The set( ) and get( ) methods simply store and produce the value, and the cast is checked at the point of the call to get( ). Now incorporate generics into the above code:
```java
//: generics/GenericHolder.java
public class GenericHolder<T> {
private T obj;
public void set(T obj) { this.obj = obj; }
public T get() { return obj; }
public static void main(String[] args) {
GenericHolder<String> holder =
new GenericHolder<String>();
holder.set("Item");
String s = holder.get();
}
} ///:~
```
The need for the cast from get( ) has disappeared, but we also know that the value passed to set( ) is being type-checked at compile time. Here are the relevant bytecodes:

<!--p493-->
```java
public void set(java.lang.Object);
0: aload_0
1: aload_1
2: putfield #2; //Field obj:Object;
5: return
public java.lang.Object get();
0: aload_0
1: getfield #2; //Field obj:Object;
4: areturn
public static void main(java.lang.String[]);
0: new #3; //class GenericHolder
3: dup
4: invokespecial #4; //Method "<init>":()V
7: astore_1
8: aload_1
9: ldc #5; //String Item
11: invokevirtual #6; //Method set:(Object;)V
14: aload_1
15: invokevirtual #7; //Method get:()Object;
18: checkcast #8; //class java/lang/String
21: astore_2
22: return
```
The resulting code is identical. The extra work of checking the incoming type in set( ) is free, because it is performed by the compiler. And the cast for the outgoing value of get( ) is still there, but it’s no less than you’d have to do yourself—and it’s automatically inserted by the compiler, so the code you write (and read) is less noisy. Since get( ) and set( ) produce the same bytecodes, all the action in generics happens at the boundaries—the extra compile-time check for incoming values, and the inserted cast for outgoing values. It helps to counter the confusion of erasure to remember that "the boundaries are where the action takes place." Compensating for erasure As we’ve seen, erasure loses the ability to perform certain operations in generic code. Anything that requires the knowledge of the exact type at run time won’t work:
```java
//: generics/Erased.java
// {CompileTimeError} (Won’t compile)
public class Erased<T> {
private final int SIZE = 100;
public static void f(Object arg) {
if(arg instanceof T) {} // Error
T var = new T(); // Error
T[] array = new T[SIZE]; // Error
T[] array = (T)new Object[SIZE]; // Unchecked warning
}
} ///:~
```
Occasionally you can program around these issues, but sometimes you must compensate for erasure by introducing a type tag. This means you explicitly pass in the Class object for your type so that you can use it in type expressions. For example, the attempt to use instanceof in the previous program fails because the type information has been erased. If you introduce a type tag, a dynamic islnstance( ) can be used instead:
```java
//: generics/ClassTypeCapture.java
class Building {}
class House extends Building {}
public class ClassTypeCapture<T> {
Class<T> kind;
public ClassTypeCapture(Class<T> kind) {
this.kind = kind;
}
```

<!--p494-->
Generics
```java
public boolean f(Object arg) {
return kind.isInstance(arg);
}
public static void main(String[] args) {
ClassTypeCapture<Building> ctt1 =
new ClassTypeCapture<Building>(Building.class);
System.out.println(ctt1.f(new Building()));
System.out.println(ctt1.f(new House()));
ClassTypeCapture<House> ctt2 =
new ClassTypeCapture<House>(House.class);
System.out.println(ctt2.f(new Building()));
System.out.println(ctt2.f(new House()));
}
} /* Output:
true
true
false
true
*///:~
```
The compiler ensures that the type tag matches the generic argument. Exercise 21: (4) Modify ClassTypeCapture.java by adding a Map<String,Class<?>>, a method addType(String typename, Class<?> kind), and a method createNew(String typename). createNew( ) will either produce a new instance of the class associated with its argument string, or produce an error message. Creating instances of types The attempt to create a new T( ) in Erased.java won’t work, partly because of erasure, and partly because the compiler cannot verify that T has a default (no-arg) constructor. But in C++ this operation is natural, straightforward, and safe (it’s checked at compile time):

<!--p495-->
```java
//: generics/InstantiateGenericType.cpp
// C++, not Java!
template<class T> class Foo {
T x; // Create a field of type T
T* y; // Pointer to T
public:
// Initialize the pointer:
Foo() { y = new T(); }
};
class Bar {};
int main() {
Foo<Bar> fb;
Foo<int> fi; // ... and it works with primitives
} ///:~
```
The solution in Java is to pass in a factory object, and use that to make the new instance. A convenient factory object is just the Class object, so if you use a type tag, you can use newlnstance( ) to create a new object of that type:
```java
//: generics/InstantiateGenericType.java
import static net.mindview.util.Print.*;
class ClassAsFactory<T> {
T x;
public ClassAsFactory(Class<T> kind) {
try {
x = kind.newInstance();
} catch(Exception e) {
throw new RuntimeException(e);
}
}
}
class Employee {}
public class InstantiateGenericType {
public static void main(String[] args) {
ClassAsFactory<Employee> fe =
new ClassAsFactory<Employee>(Employee.class);
print("ClassAsFactory<Employee> succeeded");
try {
ClassAsFactory<Integer> fi =
new ClassAsFactory<Integer>(Integer.class);
} catch(Exception e) {
print("ClassAsFactory<Integer> failed");
}
}
} /* Output:
ClassAsFactory<Employee> succeeded
ClassAsFactory<Integer> failed
*///:~
```
This compiles, but fails with ClassAsFactory<Integer> because Integer has no default constructor. Because the error is not caught at compile time, this approach is frowned upon by the Sun folks. They suggest instead that you use an explicit factory and constrain the type so that it only takes a class that implements this factory:
```java
//: generics/FactoryConstraint.java
interface FactoryI<T> {
T create();
}
class Foo2<T> {
private T x;
public <F extends FactoryI<T>> Foo2(F factory) {
x = factory.create();
}
// ...
}
class IntegerFactory implements FactoryI<Integer> {
public Integer create() {
return new Integer(0);
}
}
```

<!--p496-->
Generics
```java
class Widget {
public static class Factory implements FactoryI<Widget> {
public Widget create() {
return new Widget();
}
}
}
public class FactoryConstraint {
public static void main(String[] args) {
new Foo2<Integer>(new IntegerFactory());
new Foo2<Widget>(new Widget.Factory());
}
} ///:~
```
Note that this is really just a variation of passing Class<T>. Both approaches pass factory objects; Class<T> happens to be the built-in factory object, whereas the above approach creates an explicit factory object. But you get compile-time checking. Another approach is the Template Method design pattern. In the following example, get( ) is the Template Method, and create( ) is defined in the subclass to produce an object of that type:
```java
//: generics/CreatorGeneric.java
abstract class GenericWithCreate<T> {
final T element;
GenericWithCreate() { element = create(); }
abstract T create();
}
class X {}
class Creator extends GenericWithCreate<X> {
X create() { return new X(); }
void f() {
System.out.println(element.getClass().getSimpleName());
}
}
public class CreatorGeneric {
public static void main(String[] args) {
Creator c = new Creator();
c.f();
}
} /* Output:
X
*///:~
```

<!--p497-->
Exercise 22:(6) Use a type tag along with reflection to create a method that uses the argument version of newInstance( ) to create an object of a class with a constructor that has arguments. Exercise 23: (1) Modify FactoryConstraint.java so that create( ) takes an argument. Exercise 24:(3) Modify Exercise 21 so that factory objects are held in the Map instead of Class<?>. Arrays of generics As you saw in Erased.java, you can’t create arrays of generics. The general solution is to use an ArrayList everywhere that you are tempted to create an array of generics:
```java
//: generics/ListOfGenerics.java
import java.util.*;
public class ListOfGenerics<T> {
private List<T> array = new ArrayList<T>();
public void add(T item) { array.add(item); }
public T get(int index) { return array.get(index); }
} ///:~
```
Here you get the behavior of an array but the compile-time type safety afforded by generics. At times, you will still want to create an array of generic types (the ArrayList, for example, uses arrays internally). Interestingly enough, you can define a reference in a way that makes the compiler happy. For example:
```java
//: generics/ArrayOfGenericReference.java
class Generic<T> {}
public class ArrayOfGenericReference {
static Generic<Integer>[] gia;
} ///:~
```
The compiler accepts this without producing warnings. But you can never create an array of that exact type (including the type parameters), so it’s a little confusing. Since all arrays have the same structure (size of each array slot and array layout) regardless of the type they hold, it seems that you should be able to create an array of Object and cast that to the desired array type. This does in fact compile, but it won’t run; it produces a ClassCastException:
```java
//: generics/ArrayOfGeneric.java
public class ArrayOfGeneric {
static final int SIZE = 100;
static Generic<Integer>[] gia;
@SuppressWarnings("unchecked")
public static void main(String[] args) {
// Compiles; produces ClassCastException:
//! gia = (Generic<Integer>[])new Object[SIZE];
// Runtime type is the raw (erased) type:
gia = (Generic<Integer>[])new Generic[SIZE];
System.out.println(gia.getClass().getSimpleName());
gia[0] = new Generic<Integer>();
//! gia[1] = new Object(); // Compile-time error
// Discovers type mismatch at compile time:
//! gia[2] = new Generic<Double>();
}
} /* Output:
Generic[]
*///:~
```

<!--p498-->
The problem is that arrays keep track of their actual type, and that type is established at the point of creation of the array. So even though gia has been cast to a Generic < Integer >[], that information only exists at compile time (and without the @SuppressWarnings annotation, you’d get a warning for that cast). At run time, it’s still an array of Object, and Generics that causes problems. The only way to successfully create an array of a generic type is to create a new array of the erased type, and cast that. Let’s look at a slightly more sophisticated example. Consider a simple generic wrapper around an array:
```java
//: generics/GenericArray.java
public class GenericArray<T> {
private T[] array;
@SuppressWarnings("unchecked")
public GenericArray(int sz) {
array = (T[])new Object[sz];
}
public void put(int index, T item) {
array[index] = item;
}
public T get(int index) { return array[index]; }
// Method that exposes the underlying representation:
public T[] rep() { return array; }
public static void main(String[] args) {
GenericArray<Integer> gai =
new GenericArray<Integer>(10);
// This causes a ClassCastException:
//! Integer[] ia = gai.rep();
// This is OK:
Object[] oa = gai.rep();
}
} ///:~
```
As before, we can’t say T[] array = new T[sz], so we create an array of objects and cast it. The rep( ) method returns a T[], which in main( ) should be an Integer[] for gai, but if you call it and try to capture the result as an Integer [] reference, you get a ClassCastException, again because the actual runtime type is Object[]. If you compile GenericArray .Java after commenting out the @SuppressWarnings annotation, the compiler produces a warning:
```java
Note: GenericArray.Java uses unchecked or unsafe operations.
Note: Recompile with -Xlint:unchecked for details.
```
In this case, we’ve gotten a single warning, and we believe that it’s about the cast. But if you really want to make sure, you should compile with -Xlint:unchecked:
```java
GenericArray.java:7: warning: [unchecked] unchecked cast
found : java.lang.Object[]
required: T[]
array = (T[])new Object[sz];
^
1 warning
```

<!--p499-->
It is indeed complaining about that cast. Because warnings become noise, the best thing we could possibly do, once we verify that a particular warning is expected, is to turn it off using @SuppressWarnings. That way, when a warning does appear, we’ll actually investigate it. Because of erasure, the runtime type of the array can only be Object[]. If we immediately cast it to T[], then at compile time the actual type of the array is lost, and the compiler may miss out on some potential error checks. Because of this, it’s better to use an Object[] inside the collection, and add a cast to T when you use an array element. Let’s see how that would look with the GenericArray.java example:
```java
//: generics/GenericArray2.java
public class GenericArray2<T> {
private Object[] array;
public GenericArray2(int sz) {
array = new Object[sz];
}
public void put(int index, T item) {
array[index] = item;
}
@SuppressWarnings("unchecked")
public T get(int index) { return (T)array[index]; }
@SuppressWarnings("unchecked")
public T[] rep() {
return (T[])array; // Warning: unchecked cast
}
public static void main(String[] args) {
GenericArray2<Integer> gai =
new GenericArray2<Integer>(10);
for(int i = 0; i < 10; i ++)
gai.put(i, i);
for(int i = 0; i < 10; i ++)
System.out.print(gai.get(i) + " ");
System.out.println();
try {
Integer[] ia = gai.rep();
} catch(Exception e) { System.out.println(e); }
}
} /* Output: (Sample)
0 1 2 3 4 5 6 7 8 9
java.lang.ClassCastException: [Ljava.lang.Object; cannot be cast to
[Ljava.lang.Integer;
*///:~
```
Initially, this doesn’t look very different, just that the cast has been moved. Without the ©SuppressWarnings annotations, you will still get "unchecked" warnings. However, the internal representation is now Object[] rather than T[]. When get( ) is called, it casts the object to T, which is in fact the correct type, so that is safe. However, if you call rep( ), it again attempts to cast the Object[] to a T[], which is still incorrect, and produces a warning at compile time and an exception at run time. Thus there’s no way to subvert the type of the underlying array, which can only be Object[]. The advantage of treating array internally as Object[] instead of T[] is that it’s less likely that you’ll forget the runtime type of the array and accidentally introduce a bug (although the majority, and perhaps all, of such bugs would be rapidly detected at run time). For new code, you should pass in a type token. In that case, the GenericArray looks like this:
```java
//: generics/GenericArrayWithTypeToken.java
import java.lang.reflect.*;
public class GenericArrayWithTypeToken<T> {
private T[] array;
@SuppressWarnings("unchecked")
public GenericArrayWithTypeToken(Class<T> type, int sz) {
```

<!--p500-->
Generics
```java
array = (T[])Array.newInstance(type, sz);
}
public void put(int index, T item) {
array[index] = item;
}
public T get(int index) { return array[index]; }
// Expose the underlying representation:
public T[] rep() { return array; }
public static void main(String[] args) {
GenericArrayWithTypeToken<Integer> gai =
new GenericArrayWithTypeToken<Integer>(
Integer.class, 10);
// This now works:
Integer[] ia = gai.rep();
}
} ///:~
```
The type token Class<T> is passed into the constructor in order to recover from the erasure, so that we can create the actual type of array that we need, although the warning from the cast must be suppressed with @SuppressWarnings. Once we do get the actual type, we can return it and get the desired results, as you see in main( ). The runtime type of the array is the exact type T[]. Unfortunately, if you look at the source code in the Java SE5 standard libraries, you’ll see there are casts from Object arrays to parameterized types everywhere. For example, here’s the copy-ArrayList-from-Collection constructor, after cleaning up and simplifying:
```java
public ArrayList(Collection c) {
size = c.size();
elementData = (E[])new Object[size];
c.toArray(elementData);
}
```
If you look through ArrayList.java, you’ll find plenty of these casts. And what happens when we compile it?
```java
Note: ArrayList.java uses unchecked or unsafe operations.
Note: Recompile with -Xlint:unchecked for details.
```

<!--p501-->
Sure enough, the standard libraries produce lots of warnings. If you’ve worked with C, especially pre-ANSI C, you remember a particular effect of warnings: When you discover you can ignore them, you do. For that reason, it’s best to not issue any kind of message from the compiler unless the programmer must do something about it. In his weblog,3 Neal Gafter (one of the lead developers for Java SE5) points out that he was lazy when rewriting the Java libraries, and that we should not do what he did. Neal also points out that he could not fix some of the Java library code without breaking the existing interface. So even if certain idioms appear in the Java library sources, that’s not necessarily the right way to do it. When you look at library code, you cannot assume that it’s an example that you should follow in your own code. 3 http://gafter.blogspot.com/2004/og/puzzling-through-erasure-answer.html Bounds Bounds were briefly introduced earlier in the chapter (see page 652). Bounds allow you to place constraints on the parameter types that can be used with generics. Although this allows you to enforce rules about the types that your generics can be applied to, a potentially more important effect is that you can call methods that are in your bound types. Because erasure removes type information, the only methods you can call for an unbounded generic parameter are those available for Object. If, however, you are able to constrain that parameter to be a subset of types, then you can call the methods in that subset. To perform this constraint, Java generics reuse the extends keyword. It’s important for you to understand that extends has a significantly different meaning in the context of generic bounds than it does ordinarily. This example shows the basics of bounds:
```java
//: generics/BasicBounds.java
interface HasColor { java.awt.Color getColor(); }
class Colored<T extends HasColor> {
T item;
Colored(T item) { this.item = item; }
T getItem() { return item; }
// The bound allows you to call a method:
java.awt.Color color() { return item.getColor(); }
}
class Dimension { public int x, y, z; }
// This won’t work -- class must be first, then interfaces:
// class ColoredDimension<T extends HasColor & Dimension> {
// Multiple bounds:
class ColoredDimension<T extends Dimension & HasColor> {
T item;
ColoredDimension(T item) { this.item = item; }
T getItem() { return item; }
java.awt.Color color() { return item.getColor(); }
int getX() { return item.x; }
int getY() { return item.y; }
int getZ() { return item.z; }
}
interface Weight { int weight(); }
// As with inheritance, you can have only one
// concrete class but multiple interfaces:
class Solid<T extends Dimension & HasColor & Weight> {
T item;
Solid(T item) { this.item = item; }
T getItem() { return item; }
java.awt.Color color() { return item.getColor(); }
int getX() { return item.x; }
int getY() { return item.y; }
int getZ() { return item.z; }
int weight() { return item.weight(); }
}
class Bounded
extends Dimension implements HasColor, Weight {
public java.awt.Color getColor() { return null; }
```

<!--p502-->
Generics
```java
public int weight() { return 0; }
}
public class BasicBounds {
public static void main(String[] args) {
Solid<Bounded> solid =
new Solid<Bounded>(new Bounded());
solid.color();
solid.getY();
solid.weight();
}
} ///:~
```
You might observe that BasicBounds.java seems to contain redundancies that could be eliminated through inheritance. Here, you can see how each level of inheritance also adds bounds constraints:
```java
//: generics/InheritBounds.java
class HoldItem<T> {
T item;
HoldItem(T item) { this.item = item; }
T getItem() { return item; }
}
class Colored2<T extends HasColor> extends HoldItem<T> {
Colored2(T item) { super(item); }
java.awt.Color color() { return item.getColor(); }
}
class ColoredDimension2<T extends Dimension & HasColor>
extends Colored2<T> {
ColoredDimension2(T item) { super(item); }
int getX() { return item.x; }
int getY() { return item.y; }
int getZ() { return item.z; }
}
class Solid2<T extends Dimension & HasColor & Weight>
extends ColoredDimension2<T> {
Solid2(T item) { super(item); }
int weight() { return item.weight(); }
}
public class InheritBounds {
public static void main(String[] args) {
Solid2<Bounded> solid2 =
new Solid2<Bounded>(new Bounded());
solid2.color();
solid2.getY();
solid2.weight();
}
} ///:~
```

<!--p503-->
Holdltem simply holds an object, so this behavior is inherited into Colored2, which also requires that its parameter conforms to HasColor. ColoredDimension2 and Solid2 further extend the hierarchy and add bounds at each level. Now the methods are inherited and they don’t have to be repeated in each class. Here’s an example with more layers:
```java
//: generics/EpicBattle.java
// Demonstrating bounds in Java generics.
import java.util.*;
interface SuperPower {}
interface XRayVision extends SuperPower {
void seeThroughWalls();
}
interface SuperHearing extends SuperPower {
void hearSubtleNoises();
}
interface SuperSmell extends SuperPower {
void trackBySmell();
}
class SuperHero<POWER extends SuperPower> {
POWER power;
SuperHero(POWER power) { this.power = power; }
POWER getPower() { return power; }
}
class SuperSleuth<POWER extends XRayVision>
extends SuperHero<POWER> {
SuperSleuth(POWER power) { super(power); }
void see() { power.seeThroughWalls(); }
}
class CanineHero<POWER extends SuperHearing & SuperSmell>
extends SuperHero<POWER> {
CanineHero(POWER power) { super(power); }
void hear() { power.hearSubtleNoises(); }
void smell() { power.trackBySmell(); }
}
class SuperHearSmell implements SuperHearing, SuperSmell {
public void hearSubtleNoises() {}
public void trackBySmell() {}
}
class DogBoy extends CanineHero<SuperHearSmell> {
DogBoy() { super(new SuperHearSmell()); }
}
public class EpicBattle {
// Bounds in generic methods:
static <POWER extends SuperHearing>
void useSuperHearing(SuperHero<POWER> hero) {
hero.getPower().hearSubtleNoises();
}
static <POWER extends SuperHearing & SuperSmell>
void superFind(SuperHero<POWER> hero) {
hero.getPower().hearSubtleNoises();
hero.getPower().trackBySmell();
}
public static void main(String[] args) {
DogBoy dogBoy = new DogBoy();
useSuperHearing(dogBoy);
superFind(dogBoy);
// You can do this:
List<? extends SuperHearing> audioBoys;
// But you can’t do this:
```

<!--p504-->
Generics
```java
// List<? extends SuperHearing & SuperSmell> dogBoys;
}
} ///:~
```
Notice that wildcards (which we shall study next) are limited to a single bound. Exercise 25:(2) Create two interfaces and a class that implements both. Create two generic methods, one whose argument parameter is bounded by the first interface and one whose argument parameter is bounded by the second interface. Create an instance of the class that implements both interfaces, and show that it can be used with both generic methods. Wildcards You’ve already seen some simple uses of wildcards—question marks in generic argument expressions—in the Holding Your Objects chapter and more in the Type Information chapter. This section will explore the issue more deeply. We’ll start with an example that shows a particular behavior of arrays: You can assign an array of a derived type to an array reference of the base type:
```java
//: generics/CovariantArrays.java
class Fruit {}
class Apple extends Fruit {}
class Jonathan extends Apple {}
class Orange extends Fruit {}
public class CovariantArrays {
public static void main(String[] args) {
Fruit[] fruit = new Apple[10];
fruit[0] = new Apple(); // OK
fruit[1] = new Jonathan(); // OK
// Runtime type is Apple[], not Fruit[] or Orange[]:
try {
// Compiler allows you to add Fruit:
fruit[0] = new Fruit(); // ArrayStoreException
} catch(Exception e) { System.out.println(e); }
try {
// Compiler allows you to add Oranges:
fruit[0] = new Orange(); // ArrayStoreException
} catch(Exception e) { System.out.println(e); }
}
} /* Output:
java.lang.ArrayStoreException: Fruit
java.lang.ArrayStoreException: Orange
*///:~
```

<!--p505-->
The first line in main( ) creates an array of Apple and assigns it to a reference to an array of Fruit. This makes sense—an Apple is a kind of Fruit, so an array of Apple should also be an array of Fruit. However, if the actual array type is Apple [], you should only be able to place an Apple or a subtype of Apple into the array, which in fact works at both compile time and run time. But notice that the compiler allows you to place a Fruit object into the array. This makes sense to the compiler, because it has a Fruit[] reference—why shouldn’t it allow a Fruit object, or anything descended from Fruit, such as Orange, to be placed into the array? So at compile time, this is allowed. The runtime array mechanism, however, knows that it’s dealing with an Apple [] and throws an exception when a foreign type is placed into the array. "Upcast" is actually rather a misnomer here. What you’re really doing is assigning one array to another. The array behavior is that it holds other objects, but because we are able to upcast, it’s clear that the array objects can preserve the rules about the type of objects they contain. It’s as if the arrays are conscious of what they are holding, so between the compile- time checks and the runtime checks, you can’t abuse them. This arrangement for arrays is not so terrible, because you do find out at run time that you’ve inserted an improper type. But one of the primary goals of generics is to move such error detection to compile time. So what happens when we try to use generic containers instead of arrays?
```java
//: generics/NonCovariantGenerics.java
// {CompileTimeError} (Won’t compile)
import java.util.*;
public class NonCovariantGenerics {
// Compile Error: incompatible types:
List<Fruit> flist = new ArrayList<Apple>();
```
Although you may at first read this as saying, "You can’t assign a container of Apple to a container of Fruit," remember that generics are not just about containers. What it’s really saying is, "You can’t assign a generic involving Apples to a generic involving Fruit." If, as in the case of arrays, the compiler knew enough about the code to determine that containers were involved, perhaps it could give some leeway. But it doesn’t know anything like that, so it refuses to allow the "upcast." But it really isn’t an "upcast" anyway—a List of Apple is not a List of Fruit. A List of Apple will hold Apples and subtypes of Apple, and a List of Fruit will hold any kind of Fruit. Yes, including Apples, but that doesn’t make it a List of Apple; it’s still a List of Fruit. A List of Apple is not type-equivalent to a List of Fruit, even if an Apple is a type of Fruit. The real issue is that we are talking about the type of the container, rather than the type that the container is holding. Unlike arrays, generics do not have built-in covariance. This is because arrays are completely defined in the language and can thus have both compile-time and runtime checks built in, but with generics, the compiler and runtime system cannot know what you want to do with your types and what the rules should be. Sometimes, however, you’d like to establish some kind of upcasting relationship between the two. This is what wildcards allow.
```java
//: generics/GenericsAndCovariance.java
import java.util.*;
public class GenericsAndCovariance {
public static void main(String[] args) {
// Wildcards allow covariance:
List<? extends Fruit> flist = new ArrayList<Apple>();
// Compile Error: can’t add any type of object:
// flist.add(new Apple());
// flist.add(new Fruit());
// flist.add(new Object());
flist.add(null); // Legal but uninteresting
// We know that it returns at least Fruit:
Fruit f = flist.get(0);
}
} ///:~
```

<!--p506-->
Generics The type of flist is now List<? extends Fruit>, which you can read as "a list of any type that’s inherited from Fruit." This doesn’t actually mean that the List will hold any type of Fruit, however. The wildcard refers to a definite type, so it means "some specific type which the flist reference doesn’t specify." So the List that’s assigned has to be holding some specified type such as Fruit or Apple, but in order to upcast to flist, that type is a "don’t actually care." If the only constraint is that the List hold a specific Fruit or subtype of Fruit, but you don’t actually care what it is, then what can you do with such a List? If you don’t know what type the List is holding, how can you safely add an object? Just as with the "upcast" array in CovariantArrays.java, you can’t, except that the compiler prevents it from happening rather than the runtime system. You discover the problem sooner. You might argue that things have gone a bit overboard, because now you can’t even add an Apple to a List that you just said would hold Apples. Yes, but the compiler doesn’t know that. A List<? extends Fruit> could legally point to a List<Orange>. Once you do this kind of "upcast," you lose the ability to pass anything in, even an Object. On the other hand, if you call a method that returns Fruit, that’s safe because you know that anything in the List must at least be of type Fruit, so the compiler allows it. Exercise 26: (2) Demonstrate array covariance using Numbers and Integers. Exercise 27: (2) Show that covariance doesn’t work with Lists, using Numbers and Integers, then introduce wildcards. How smart is the compiler? Now, you might guess that you are prevented from calling any methods that take arguments, but consider this:
```java
//: generics/CompilerIntelligence.java
import java.util.*;
public class CompilerIntelligence {
public static void main(String[] args) {
List<? extends Fruit> flist =
Arrays.asList(new Apple());
Apple a = (Apple)flist.get(0); // No warning
flist.contains(new Apple()); // Argument is ‘Object’
flist.indexOf(new Apple()); // Argument is ‘Object’
}
} ///:~
```

<!--p507-->
You can see calls to contains( ) and indexOf( ) that take Apple objects as arguments, and those are just fine. Does this mean that the compiler actually examines the code to see if a particular method modifies its object? By looking at the documentation for ArrayList, we find that the compiler is not that smart. While add( ) takes an argument of the generic parameter type, contains( ) and indexOf( ) take arguments of type Object. So when you specify an ArrayList <? extends Fruit >, the argument for add( ) becomes’? extends Fruit’. From that description, the compiler cannot know which specific subtype of Fruit is required there, so it won’t accept any type of Fruit. It doesn’t matter if you upcast the Apple to a Fruit first—the compiler simply refuses to call a method (such as add( )) if a wildcard is involved in the argument list. With contains( ) and indexOf( ), the arguments are of type Object, so there are no wildcards involved and the compiler allows the call. This means that it’s up to the generic class designer to decide which calls are "safe," and to use Object types for their arguments. To disallow a call when the type is used with wildcards, use the type parameter in the argument list. You can see this in a very simple Holder class:
```java
//: generics/Holder.java
public class Holder<T> {
private T value;
public Holder() {}
public Holder(T val) { value = val; }
public void set(T val) { value = val; }
public T get() { return value; }
public boolean equals(Object obj) {
return value.equals(obj);
}
public static void main(String[] args) {
Holder<Apple> Apple = new Holder<Apple>(new Apple());
Apple d = Apple.get();
Apple.set(d);
// Holder<Fruit> Fruit = Apple; // Cannot upcast
Holder<? extends Fruit> fruit = Apple; // OK
Fruit p = fruit.get();
d = (Apple)fruit.get(); // Returns ‘Object’
try {
Orange c = (Orange)fruit.get(); // No warning
} catch(Exception e) { System.out.println(e); }
// fruit.set(new Apple()); // Cannot call set()
// fruit.set(new Fruit()); // Cannot call set()
System.out.println(fruit.equals(d)); // OK
}
} /* Output: (Sample)
java.lang.ClassCastException: Apple cannot be cast to Orange
true
*///:~
```

<!--p508-->
Holder has a set( ) which takes a T, a get( ) which returns a T, and an equals( ) that takes an Object. As you’ve already seen, if you create a Holder<Apple>, you cannot upcast it to a Holder<Fruit>, but you can upcast to a Holder<? extends Fruit>. If you call get( ), it only returns a Fruit—that’s as much as it knows given the "anything that extends Fruit" bound. If you know more about what’s there, you can cast to a specific type of Fruit and there won’t be any warning about it, but you risk a ClassCastException. The set( ) method won’t work with either an Apple or a Fruit, because the set( ) argument is also "? Extends Fruit," which means it can be anything and the compiler can’t verify type safety for "anything." However, the equals( ) method works fine because it takes an Object instead of a T as an argument. Thus, the compiler is only paying attention to the types of objects that are passed and returned. It is not analyzing the code to see if you perform any actual writes or reads. Contravariance It’s also possible to go the other way, and use supertype wildcards. Here, you say that the wildcard is bounded by any base class of a particular class, by specifying <? super MyClass> or even using a type parameter: <? super T> (although you cannot give a generic parameter a supertype bound; that is, you cannot say <T super MyClass>). This Generics allows you to safely pass a typed object into a generic type. Thus, with supertype wildcards you can write into a Collection:
```java
//: generics/SuperTypeWildcards.java
import java.util.*;
public class SuperTypeWildcards {
static void writeTo(List<? super Apple> apples) {
apples.add(new Apple());
apples.add(new Jonathan());
// apples.add(new Fruit()); // Error
}
} ///:~
```
The argument apples is a List of some type that is the base type of Apple; thus you know that it is safe to add an Apple or a subtype of Apple. Since the lower bound is Apple, however, you don’t know that it is safe to add Fruit to such a List, because that would allow the List to be opened up to the addition of non-Apple types, which would violate static type safety. You can thus begin to think of subtype and supertype bounds in terms of how you can "write" (pass into a method) to a generic type, and "read" (return from a method) from a generic type. Supertype bounds relax the constraints on what you can pass into a method:
```java
//: generics/GenericWriting.java
import java.util.*;
public class GenericWriting {
static <T> void writeExact(List<T> list, T item) {
list.add(item);
}
static List<Apple> apples = new ArrayList<Apple>();
static List<Fruit> fruit = new ArrayList<Fruit>();
static void f1() {
writeExact(apples, new Apple());
// writeExact(fruit, new Apple()); // Error:
// Incompatible types: found Fruit, required Apple
}
static <T> void
writeWithWildcard(List<? super T> list, T item) {
list.add(item);
}
static void f2() {
writeWithWildcard(apples, new Apple());
writeWithWildcard(fruit, new Apple());
}
public static void main(String[] args) { f1(); f2(); }
} ///:~
```

<!--p509-->
The writeExact( ) method uses an exact parameter type (no wildcards). In fi( ) you can see that this works fine—as long as you only put an Apple into a List<Apple>. However, writeExact( ) does not allow you to put an Apple into a List<Fruit>, even though you know that should be possible. In writeWithWildcard( ), the argument is now a List<? super T>, so the List holds a specific type that is derived from T; thus it is safe to pass a T or anything derived from T as an argument to List methods. You can see this in f2( ), where it’s still possible to put an Apple into a List<Apple>, as before, but it is now also possible to put an Apple into a List<Fruit>, as you expect. We can perform this same type of analysis as a review of covariance and wildcards:
```java
//: generics/GenericReading.java
import java.util.*;
public class GenericReading {
static <T> T readExact(List<T> list) {
return list.get(0);
}
static List<Apple> apples = Arrays.asList(new Apple());
static List<Fruit> fruit = Arrays.asList(new Fruit());
// A static method adapts to each call:
static void f1() {
Apple a = readExact(apples);
Fruit f = readExact(fruit);
f = readExact(apples);
}
// If, however, you have a class, then its type is
// established when the class is instantiated:
static class Reader<T> {
T readExact(List<T> list) { return list.get(0); }
}
static void f2() {
Reader<Fruit> fruitReader = new Reader<Fruit>();
Fruit f = fruitReader.readExact(fruit);
// Fruit a = fruitReader.readExact(apples); // Error:
// readExact(List<Fruit>) cannot be
// applied to (List<Apple>).
}
static class CovariantReader<T> {
T readCovariant(List<? extends T> list) {
return list.get(0);
}
}
static void f3() {
CovariantReader<Fruit> fruitReader =
new CovariantReader<Fruit>();
Fruit f = fruitReader.readCovariant(fruit);
Fruit a = fruitReader.readCovariant(apples);
}
public static void main(String[] args) {
f1(); f2(); f3();
}
} ///:~
```

<!--p510-->
As before, the first method readExact( ) uses the precise type. So if you use the precise type with no wildcards, you can both write and read that precise type into and out of a List. In addition, for the return value, the static generic method readExact( ) effectively "adapts" to each method call, and returns an Apple from a List<Apple> and a Fruit from a List<Fruit>, as you can see in f1( ). Thus, if you can get away with a static generic method, you don’t necessarily need covariance if you’re just reading. If you have a generic class, however, the parameter is established for the class when you make an instance of that class. As you can see in f2( ), the fruitReader instance can read a piece of Fruit from a List<Fruit>, since that is its exact type. But a List<Apple> should also produce Fruit objects, and the fruitReader doesn’t allow this. Generics To fix the problem, the CovariantReader.readCovariant( ) method takes a List<? extends T>, and so it’s safe to read a T from that list (you know that everything in that list is at least a T, and possibly something derived from a T). In f3( ) you can see that it’s now possible to read a Fruit from a List<Apple>. Exercise 28:(4) Create a generic class Generic1<T> with a single method that takes an argument of type T. Create a second generic class Generic2<T> with a single method that returns an argument of type T. Write a generic method with a contravariant argument of the first generic class that calls its method. Write a second generic method with a covariant argument of the second generic class that calls its method. Test using the typeinfo.pets library. Unbounded wildcards The unbounded wildcard <?> appears to mean "anything," and so using an unbounded wildcard seems equivalent to using a raw type. Indeed, the compiler seems at first to agree with this assessment:

<!--p511-->
```java
//: generics/UnboundedWildcards1.java
import java.util.*;
public class UnboundedWildcards1 {
static List list1;
static List<?> list2;
static List<? extends Object> list3;
static void assign1(List list) {
list1 = list;
list2 = list;
// list3 = list; // Warning: unchecked conversion
// Found: List, Required: List<? extends Object>
}
static void assign2(List<?> list) {
list1 = list;
list2 = list;
list3 = list;
}
static void assign3(List<? extends Object> list) {
list1 = list;
list2 = list;
list3 = list;
}
public static void main(String[] args) {
assign1(new ArrayList());
assign2(new ArrayList());
// assign3(new ArrayList()); // Warning:
// Unchecked conversion. Found: ArrayList
// Required: List<? extends Object>
assign1(new ArrayList<String>());
assign2(new ArrayList<String>());
assign3(new ArrayList<String>());
// Both forms are acceptable as List<?>:
List<?> wildList = new ArrayList();
wildList = new ArrayList<String>();
assign1(wildList);
assign2(wildList);
assign3(wildList);
}
} ///:~
```
There are many cases like the ones you see here where the compiler could care less whether you use a raw type or <?>. In those cases, <?> can be thought of as a decoration; and yet it is valuable because, in effect, it says, "I wrote this code with Java generics in mind, and I don’t mean here that I’m using a raw type, but that in this case the generic parameter can hold any type." A second example shows an important use of unbounded wildcards. When you are dealing with multiple generic parameters, it’s sometimes important to allow one parameter to be any type while establishing a particular type for the other parameter:
```java
//: generics/UnboundedWildcards2.java
import java.util.*;
public class UnboundedWildcards2 {
static Map map1;
static Map<?,?> map2;
static Map<String,?> map3;
static void assign1(Map map) { map1 = map; }
static void assign2(Map<?,?> map) { map2 = map; }
static void assign3(Map<String,?> map) { map3 = map; }
public static void main(String[] args) {
assign1(new HashMap());
assign2(new HashMap());
// assign3(new HashMap()); // Warning:
// Unchecked conversion. Found: HashMap
// Required: Map<String,?>
assign1(new HashMap<String,Integer>());
assign2(new HashMap<String,Integer>());
assign3(new HashMap<String,Integer>());
}
} ///:~
```
But again, when you have all unbounded wildcards, as seen in Map<?,?>, the compiler doesn’t seem to distinguish it from a raw Map. In addition, UnboundedWildcards1.java shows that the compiler treats List<?> and List<? extends Object> differently. What’s confusing is that the compiler doesn’t always care about the difference between, for example, List and List<?>, so they can seem like the same thing. Indeed, since a generic argument erases to its first bound, List<?> would seem to be equivalent to List<Object>, and List is effectively List<Object> as well—except neither of those statements is exactly true. List actually means "a raw List that holds any Object type," whereas List<?> means "a non-raw List of some specific type, but we just don’t know what that type is." When does the compiler actually care about the difference between raw types and types involving unbounded wildcards? The following example uses the previously defined Holder<T> class. It contains methods that take Holder as an argument, but in various forms: as a raw type, with a specific type parameter, and with an unbounded wildcard parameter:
```java
//: generics/Wildcards.java
// Exploring the meaning of wildcards.
public class Wildcards {
// Raw argument:
static void rawArgs(Holder holder, Object arg) {
// holder.set(arg); // Warning:
// Unchecked call to set(T) as a
// member of the raw type Holder
// holder.set(new Wildcards()); // Same warning
```

<!--p512-->
Generics

<!--p513-->
```java
// Can’t do this; don’t have any ‘T’:
// T t = holder.get();
// OK, but type information has been lost:
Object obj = holder.get();
}
// Similar to rawArgs(), but errors instead of warnings:
static void unboundedArg(Holder<?> holder, Object arg) {
// holder.set(arg); // Error:
// set(capture of ?) in Holder<capture of ?>
// cannot be applied to (Object)
// holder.set(new Wildcards()); // Same error
// Can’t do this; don’t have any ‘T’:
// T t = holder.get();
// OK, but type information has been lost:
Object obj = holder.get();
}
static <T> T exact1(Holder<T> holder) {
T t = holder.get();
return t;
}
static <T> T exact2(Holder<T> holder, T arg) {
holder.set(arg);
T t = holder.get();
return t;
}
static <T>
T wildSubtype(Holder<? extends T> holder, T arg) {
// holder.set(arg); // Error:
// set(capture of ? extends T) in
// Holder<capture of ? extends T>
// cannot be applied to (T)
T t = holder.get();
return t;
}
static <T>
void wildSupertype(Holder<? super T> holder, T arg) {
holder.set(arg);
// T t = holder.get(); // Error:
// Incompatible types: found Object, required T
// OK, but type information has been lost:
Object obj = holder.get();
}
public static void main(String[] args) {
Holder raw = new Holder<Long>();
// Or:
raw = new Holder();
Holder<Long> qualified = new Holder<Long>();
Holder<?> unbounded = new Holder<Long>();
Holder<? extends Long> bounded = new Holder<Long>();
Long lng = 1L;
rawArgs(raw, lng);
rawArgs(qualified, lng);
rawArgs(unbounded, lng);
rawArgs(bounded, lng);
unboundedArg(raw, lng);
unboundedArg(qualified, lng);
unboundedArg(unbounded, lng);
unboundedArg(bounded, lng);
// Object r1 = exact1(raw); // Warnings:
// Unchecked conversion from Holder to Holder<T>
// Unchecked method invocation: exact1(Holder<T>)
// is applied to (Holder)
Long r2 = exact1(qualified);
Object r3 = exact1(unbounded); // Must return Object
Long r4 = exact1(bounded);
// Long r5 = exact2(raw, lng); // Warnings:
// Unchecked conversion from Holder to Holder<Long>
// Unchecked method invocation: exact2(Holder<T>,T)
// is applied to (Holder,Long)
Long r6 = exact2(qualified, lng);
// Long r7 = exact2(unbounded, lng); // Error:
// exact2(Holder<T>,T) cannot be applied to
// (Holder<capture of ?>,Long)
// Long r8 = exact2(bounded, lng); // Error:
// exact2(Holder<T>,T) cannot be applied
// to (Holder<capture of ? extends Long>,Long)
// Long r9 = wildSubtype(raw, lng); // Warnings:
// Unchecked conversion from Holder
// to Holder<? extends Long>
// Unchecked method invocation:
// wildSubtype(Holder<? extends T>,T) is
// applied to (Holder,Long)
Long r10 = wildSubtype(qualified, lng);
// OK, but can only return Object:
Object r11 = wildSubtype(unbounded, lng);
Long r12 = wildSubtype(bounded, lng);
// wildSupertype(raw, lng); // Warnings:
// Unchecked conversion from Holder
// to Holder<? super Long>
// Unchecked method invocation:
// wildSupertype(Holder<? super T>,T)
// is applied to (Holder,Long)
wildSupertype(qualified, lng);
// wildSupertype(unbounded, lng); // Error:
// wildSupertype(Holder<? super T>,T) cannot be
// applied to (Holder<capture of ?>,Long)
// wildSupertype(bounded, lng); // Error:
// wildSupertype(Holder<? super T>,T) cannot be
// applied to (Holder<capture of ? extends Long>,Long)
}
} ///:~
```

<!--p514-->

<!--p515-->
In rawArgs( ), the compiler knows that Holder is a generic type, so even though it is expressed as a raw type here, the compiler knows that passing an Object to set( ) is unsafe. Since it’s a raw type, you can pass an object of any type into set( ), and that object is upcast to Object. So anytime you have a raw type, you give up compile-time checking. The call to get( ) shows the same issue: There’s no T, so the result can only be an Object. It’s easy to start thinking that a raw Holder and a Holder<?> are roughly the same thing. But unboundedArg( ) emphasizes that they are differentit discovers the same kind of problems, but reports them as errors rather than warnings, because the raw Holder will hold a combination of any types, whereas a Holder<?> holds a homogeneous collection of some specific type, and thus you can’t just pass in an Object. Generics In exact1( ) and exact2( ), you see the exact generic parameters used—no wildcards. You’ll see that exact2( ) has different limitations than exact1( ), because of the extra argument. In wildSubtype( ), the constraints on the type of Holder are relaxed to include a Holder of anything that extends T. Again, this means that T could be Fruit, while holder could legitimately be a Holder<Apple>. To prevent putting an Orange in a Holder<Apple>, the call to set( ) (or any method that takes an argument of the type parameter) is disallowed. However, you still know that anything that comes out of a Holder<? extends Fruit> will at least be Fruit, so get( ) (or any method that produces a return value of the type parameter) is allowed. Supertype wildcards are shown in wildSupertype( ), which shows the opposite behavior of wildSubtype( ): holder can be a container that holds any type that’s a base class of T. Thus, set( ) can accept a T, since anything that works with a base type will polymorphically work with a derived type (thus a T). However, trying to call get( ) is not helpful, because the type held by holder can be any supertype at all, so the only safe one is Object. This example also shows the limitations on what you can and can’t do with an unbounded parameter in unbounded( ): You can’t get( ) or set( ) a T because you don’t have a T. In main( ) you can see which of these methods can accept which types of arguments without errors and warnings. For migration compatibility, rawArgs( ) will take all the different variations of Holder without producing warnings. The unboundedArg( ) method is equally accepting of all types, although, as previously noted, it handles them differently inside the body of the method. If you pass a raw Holder reference into a method that takes an "exact" generic type (no wildcards), you get a warning because the exact argument is expecting information that doesn’t exist in the raw type. And if you pass an unbounded reference to exact1( ), there’s no type information to establish the return type. You can see that exact2( ) has the most constraints, since it wants exactly a Holder<T> and an argument of type T, and because of this it generates errors or warnings unless you give it the exact arguments. Sometimes this is OK, but if it’s overconstraining, then you can use wildcards, depending on whether you want to get typed return values from your generic argument (as seen in wildSubtype( )) or you want to pass typed arguments to your generic argument (as seen in wildSupertype( )). Thus, the benefit of using exact types instead of wildcard types is that you can do more with the generic parameters. But using wildcards allows you to accept a broader range of parameterized types as arguments. You must decide which trade-off is more appropriate for your needs on a case-by-case basis. Capture conversion One situation in particular requires the use of <?> rather than a raw type. If you pass a raw type to a method that uses <?>, it’s possible for the compiler to infer the actual type parameter, so that the method can turn around and call another method that uses the exact type. The following example demonstrates the technique, which is called capture conversion because the unspecified wildcard type is captured and converted to an exact type. Here, the comments about warnings only take effect when the @SuppressWarnings annotation is removed:
```java
//: generics/CaptureConversion.java
public class CaptureConversion {
static <T> void f1(Holder<T> holder) {
T t = holder.get();
System.out.println(t.getClass().getSimpleName());
}
static void f2(Holder<?> holder) {
f1(holder); // Call with captured type
}
@SuppressWarnings("unchecked")
public static void main(String[] args) {
Holder raw = new Holder<Integer>(1);
// f1(raw); // Produces warnings
f2(raw); // No warnings
Holder rawBasic = new Holder();
rawBasic.set(new Object()); // Warning
f2(rawBasic); // No warnings
// Upcast to Holder<?>, still figures it out:
Holder<?> wildcarded = new Holder<Double>(1.0);
f2(wildcarded);
}
} /* Output:
Integer
Object
Double
*///:~
```

<!--p516-->
The type parameters in f1( ) are all exact, without wildcards or bounds. In f2( ), the Holder parameter is an unbounded wildcard, so it would seem to be effectively unknown. However, within f2( ), f1( ) is called and f1( ) requires a known parameter. What’s happening is that the parameter type is captured in the process of calling f2( ), so it can be used in the call to f1( ). You might wonder if this technique could be used for writing, but that would require you to pass a specific type along with the Holder<?>. Capture conversion only works in situations where, within the method, you need to work with the exact type. Notice that you can’t return T from f2( ), because T is unknown for f2( ). Capture conversion is interesting, but quite limited. Exercise 29:(5) Create a generic method that takes as an argument a Holder<List<?>>. Determine what methods you can and can’t call for the Holder and for the List. Repeat for an argument of List<Holder<?>>. Issues This section addresses an assorted set of issues that appear when you are using Java generics. No primitives as type parameters As mentioned earlier in this chapter, one of the limitations you will discover in Java generics is that you cannot use primitives as type parameters. So you cannot, for example, create an ArrayList<int>. The solution is to use the primitive wrapper classes in conjunction with Java SE5 autoboxing. If you create an ArrayList< Integer> and use primitive ints with this container, you’ll Generics discover that autoboxing does the conversion to and from Integer automatically—so it’s almost as if you have an Ar r ayList < int >:
```java
//: generics/ListOfInt.java
// Autoboxing compensates for the inability to use
// primitives in generics.
import java.util.*;
public class ListOfInt {
public static void main(String[] args) {
List<Integer> li = new ArrayList<Integer>();
for(int i = 0; i < 5; i++)
li.add(i);
for(int i : li)
System.out.print(i + " ");
}
} /* Output:
0 1 2 3 4
*///:~
```
Note that autoboxing even allows the foreach syntax to produce ints. In general this solution works fine—you’re able to successfully store and retrieve ints. There happen to be some conversions going on but these are hidden from you. However, if performance is a problem, you can use a specialized version of the containers adapted for primitive types; one opensource version of this is org.apache.commons.collections.primitives. Here’s another approach, which creates a Set of Bytes:
```java
//: generics/ByteSet.java
import java.util.*;
public class ByteSet {
Byte[] possibles = { 1,2,3,4,5,6,7,8,9 };
Set<Byte> mySet =
new HashSet<Byte>(Arrays.asList(possibles));
// But you can’t do this:
// Set<Byte> mySet2 = new HashSet<Byte>(
// Arrays.<Byte>asList(1,2,3,4,5,6,7,8,9));
} ///:~
```
Notice that autoboxing solves some problems, but not all. The following example shows a generic Generator interface that specifies a next( ) that returns an object of the parameter type. The FArray class contains a generic method that uses a generator to fill an array with objects (making the class generic wouldn’t work in this case because the method is static). The Generator implementations come from the Arrays chapter, and in main( ) you can see FArray.fill( ) used to fill arrays with objects:

<!--p517-->
```java
//: generics/PrimitiveGenericTest.java
import net.mindview.util.*;
// Fill an array using a generator:
class FArray {
public static <T> T[] fill(T[] a, Generator<T> gen) {
for(int i = 0; i < a.length; i++)
a[i] = gen.next();
return a;
}
}
public class PrimitiveGenericTest {
public static void main(String[] args) {
String[] strings = FArray.fill(
new String[7], new RandomGenerator.String(10));
for(String s : strings)
System.out.println(s);
Integer[] integers = FArray.fill(
new Integer[7], new RandomGenerator.Integer());
for(int i: integers)
System.out.println(i);
// Autoboxing won’t save you here. This won’t compile:
// int[] b =
// FArray.fill(new int[7], new RandIntGenerator());
}
} /* Output:
YNzbrnyGcF
OWZnTcQrGs
eGZMmJMRoE
suEcUOneOE
dLsmwHLGEa
hKcxrEqUCB
bkInaMesbt
*///:~
```
Since RandomGenerator.Integer implements Generator<Integer>, my hope was that autoboxing would automatically convert the value of next( ) from Integer to int. However, autoboxing doesn’t apply to arrays, so this won’t work. Exercise 30:(2) Create a Holder for each of the primitive wrapper types, and show that autoboxing and autounboxing works for the set( ) and get( ) methods of each instance. Implementing parameterized interfaces A class cannot implement two variants of the same generic interface. Because of erasure, these are both the same interface. Here’s a situation where this clash occurs:
```java
//: generics/MultipleInterfaceVariants.java
// {CompileTimeError} (Won’t compile)
interface Payable<T> {}
class Employee implements Payable<Employee> {}
class Hourly extends Employee
implements Payable<Hourly> {} ///:~
```

<!--p518-->
Hourly won’t compile because erasure reduces Payable<Employee> and Payable<Hourly> to the same class, Payable, and the above code would mean that you’d be implementing the same interface twice. Interestingly enough, if you remove the generic parameters from both uses of Payable—as the compiler does during erasure—the code compiles. Generics This issue can become annoying when you are working with some of the more fundamental Java interfaces, such as Comparable<T>, as you’ll see a little later in this section. Exercise 31:(1) Remove all the generics from MultipleInterfaceVariants.java and modify the code so that the example compiles. Casting and warnings Using a cast or instanceof with a generic type parameter doesn’t have any effect. The following container stores values internally as Objects and casts them back to T when you fetch them:
```java
//: generics/GenericCast.java
class FixedSizeStack<T> {
private int index = 0;
private Object[] storage;
public FixedSizeStack(int size) {
storage = new Object[size];
}
public void push(T item) { storage[index++] = item; }
@SuppressWarnings("unchecked")
public T pop() { return (T)storage[--index]; }
}
public class GenericCast {
public static final int SIZE = 10;
public static void main(String[] args) {
FixedSizeStack<String> strings =
new FixedSizeStack<String>(SIZE);
for(String s : "A B C D E F G H I J".split(" "))
strings.push(s);
for(int i = 0; i < SIZE; i++) {
String s = strings.pop();
System.out.print(s + " ");
}
}
} /* Output:
J I H G F E D C B A
*///:~
```
Without the @SuppressWarnings annotation, the compiler will produce an "unchecked cast" warning for pop( ). Because of erasure, it can’t know whether the cast is safe, and the pop( ) method doesn’t actually do any casting. T is erased to its first bound, which is Object by default, so pop( ) is actually just casting an Object to an Object. There are times when generics do not eliminate the need to cast, and this generates a warning by the compiler which is inappropriate. For example:

<!--p519-->
```java
//: generics/NeedCasting.java
import java.io.*;
import java.util.*;
public class NeedCasting {
@SuppressWarnings("unchecked")
public void f(String[] args) throws Exception {
ObjectInputStream in = new ObjectInputStream(
new FileInputStream(args[0]));
List<Widget> shapes = (List<Widget>)in.readObject();
}
} ///:~
```
As you’ll learn in the next chapter, readObject( ) cannot know what it is reading, so it returns an object that must be cast. But when you comment out the @SuppressWarnings annotation and compile the program, you get a warning:
```java
Note: NeedCasting.Java uses unchecked or unsafe operations.
Note: Recompile with -Xlint:unchecked for details.
```
And if you follow the instructions and recompile with -Xlint:unchecked:
```java
NeedCasting.Java:12: warning: [unchecked] unchecked cast
found : java.lang.Object
required: java.uti1.List<Widget>
List<Shape> shapes = (List<Widget>)in.readObject();
```
You’re forced to cast, and yet you’re told you shouldn’t. To solve the problem, you must use a new form of cast introduced in Java SE5, the cast via a generic class:
```java
//: generics/ClassCasting.java
import java.io.*;
import java.util.*;
public class ClassCasting {
@SuppressWarnings("unchecked")
public void f(String[] args) throws Exception {
ObjectInputStream in = new ObjectInputStream(
new FileInputStream(args[0]));
// Won’t Compile:
// List<Widget> lw1 =
// List<Widget>.class.cast(in.readObject());
List<Widget> lw2 = List.class.cast(in.readObject());
}
} ///:~
```
However, you can’t cast to the actual type (List<Widget>). That is, you can’t say
```java
List<Widget>.class.cast(in.readObject())
```
and even if you add another cast like this:
```java
(List<Widget>)List.class.cast(in.readObject())
```

<!--p520-->
you’ll still get a warning. Exercise 32:(1) Verify that FixedSizeStack in GenericCast.java generates exceptions if you try to go out of its bounds. Does this mean that bounds-checking code is not required? Exercise 33:(3) Repair GenericCast.java using an ArrayList. Generics Overloading This won’t compile, even though it’s a reasonable thing to try:
```java
//: generics/UseList.java
// {CompileTimeError} (Won’t compile)
import java.util.*;
public class UseList<W,T> {
void f(List<T> v) {}
void f(List<W> v) {}
} ///:~
```
Overloading the method produces the identical type signature because of erasure. Instead, you must provide distinct method names when the erased arguments do not produce a unique argument list:
```java
//: generics/UseList2.java
import java.util.*;
public class UseList2<W,T> {
void f1(List<T> v) {}
void f2(List<W> v) {}
} ///:~
```
Fortunately, this kind of problem is detected by the compiler. Base class hijacks an interface Suppose you have a Pet class that is Comparable to other Pet objects:
```java
//: generics/ComparablePet.java
public class ComparablePet
implements Comparable<ComparablePet> {
public int compareTo(ComparablePet arg) { return 0; }
} ///:~
```
It makes sense to try to narrow the type that a subclass of ComparablePet can be compared to. For example, a Cat should only be Comparable with other Cats:
```java
//: generics/HijackedInterface.java
// {CompileTimeError} (Won’t compile)
class Cat extends ComparablePet implements Comparable<Cat>{
// Error: Comparable cannot be inherited with
// different arguments: <Cat> and <Pet>
public int compareTo(Cat arg) { return 0; }
} ///:~
```
Unfortunately, this won’t work. Once the ComparablePet argument is established for Comparable, no other implementing class can ever be compared to anything but a ComparablePet:

<!--p521-->
```java
//: generics/RestrictedComparablePets.java
class Hamster extends ComparablePet
implements Comparable<ComparablePet> {
public int compareTo(ComparablePet arg) { return 0; }
}
// Or just:
class Gecko extends ComparablePet {
public int compareTo(ComparablePet arg) { return 0; }
} ///:~
```

<!--p522-->
Hamster shows that it is possible to reimplement the same interface that is in ComparablePet, as long as it is exactly the same, including the parameter types. However, this is the same as just overriding the methods in the base class, as seen in Gecko. Generics Self-bounded types There’s one rather mind-bending idiom that appears periodically in Java generics. Here’s what it looks like:
```java
class SelfBounded<T extends SelfBounded<T>> { // ...
```
This has the dizzying effect of two mirrors pointed at each other, a kind of infinite reflection. The class SelfBounded takes a generic argument T, T is constrained by a bound, and that bound is SelfBounded, with T as an argument. This is difficult to parse when you first see it, and it emphasizes that the extends keyword, when used with bounds, is definitely different than when it is used to create subclasses. Curiously recurring generics To understand what a self-bounded type means, let’s start with a simpler version of the idiom, without the self-bound. You can’t inherit directly from a generic parameter. However, you can inherit from a class that uses that generic parameter in its own definition. That is, you can say:
```java
//: generics/CuriouslyRecurringGeneric.java
class GenericType<T> {}
public class CuriouslyRecurringGeneric
extends GenericType<CuriouslyRecurringGeneric> {} ///:~
```
This could be called curiously recurring generics (CRG) after Jim Coplien’s Curiously Recurring Template Pattern in C++. The "curiously recurring" part refers to the fact that your class appears, rather curiously, in its own base class. To understand what this means, try saying it aloud: "I’m creating a new class that inherits from a generic type that takes my class name as its parameter." What can the generic base type accomplish when given the derived class name? Well, generics in Java are about arguments and return types, so it can produce a base class that uses the derived type for its arguments and return types. It can also use the derived type for field types, even though those will be erased to Object. Here’s a generic class that expresses this:
```java
//: generics/BasicHolder.java
public class BasicHolder<T> {
T element;
void set(T arg) { element = arg; }
T get() { return element; }
void f() {
System.out.println(element.getClass().getSimpleName());
}
} ///:~
```

<!--p523-->
It’s an ordinary generic type with methods that both accept and produce objects of the parameter type, along with a method that operates on the stored field (although it only performs Object operations on that field). We can use BasicHolder in a curiously recurring generic:
```java
//: generics/CRGWithBasicHolder.java
class Subtype extends BasicHolder<Subtype> {}
public class CRGWithBasicHolder {
public static void main(String[] args) {
Subtype st1 = new Subtype(), st2 = new Subtype();
st1.set(st2);
Subtype st3 = st1.get();
st1.f();
}
} /* Output:
Subtype
*///:~
```
Notice something important here: The new class Subtype takes arguments and returns values of Subtype, not just the base class BasicHolder. This is the essence of CRG: The base class substitutes the derived class for its parameters. This means that the generic base class becomes a kind of template for common functionality for all its derived classes, but this functionality will use the derived type for all of its arguments and return values. That is, the exact type instead of the base type will be used in the resulting class. So in Subtype, both the argument to set( ) and the return type of get( ) are exactly Subtypes. Self-bounding The BasicHolder can use any type as its generic parameter, as seen here:
```java
//: generics/Unconstrained.java
class Other {}
class BasicOther extends BasicHolder<Other> {}
public class Unconstrained {
public static void main(String[] args) {
BasicOther b = new BasicOther(), b2 = new BasicOther();
b.set(new Other());
Other other = b.get();
b.f();
}
} /* Output:
Other
*///:~
```
Self-bounding takes the extra step of forcing the generic to be used as its own bound argument. Look at how the resulting class can and can’t be used:
```java
//: generics/SelfBounding.java
class SelfBounded<T extends SelfBounded<T>> {
T element;
SelfBounded<T> set(T arg) {
element = arg;
return this;
}
T get() { return element; }
}
class A extends SelfBounded<A> {}
```

<!--p524-->
Generics
```java
class B extends SelfBounded<A> {} // Also OK
class C extends SelfBounded<C> {
C setAndGet(C arg) { set(arg); return get(); }
}
class D {}
// Can’t do this:
// class E extends SelfBounded<D> {}
// Compile error: Type parameter D is not within its bound
// Alas, you can do this, so you can’t force the idiom:
class F extends SelfBounded {}
public class SelfBounding {
public static void main(String[] args) {
A a = new A();
a.set(new A());
a = a.set(new A()).get();
a = a.get();
C c = new C();
c = c.setAndGet(new C());
}
} ///:~
```
What self-bounding does is require the use of the class in an inheritance relationship like this:
```java
class A extends SelfBounded<A> {}
```
This forces you to pass the class that you are defining as a parameter to the base class. What’s the added value in self-bounding the parameter? The type parameter must be the same as the class being defined. As you can see in the definition of class B, you can also derive from a SelfBounded that uses a parameter of another SelfBounded, although the predominant use seems to be the one that you see for class A. The attempt to define E shows that you cannot use a type parameter that is not a SelfBounded. Unfortunately, F compiles without warnings, so the self-bounding idiom is not enforceable. If it’s really important, it may require an external tool to ensure that raw types are not being used in place of parameterized types. Notice that you can remove the constraint and all the classes will still compile, but E will also compile:

<!--p525-->
```java
//: generics/NotSelfBounded.java
public class NotSelfBounded<T> {
T element;
NotSelfBounded<T> set(T arg) {
element = arg;
return this;
}
T get() { return element; }
}
class A2 extends NotSelfBounded<A2> {}
class B2 extends NotSelfBounded<A2> {}
class C2 extends NotSelfBounded<C2> {
C2 setAndGet(C2 arg) { set(arg); return get(); }
}
class D2 {}
// Now this is OK:
class E2 extends NotSelfBounded<D2> {} ///:~
```
So clearly, the self-bounding constraint serves only to force the inheritance relationship. If you use self-bounding, you know that the type parameter used by the class will be the same basic type as the class that’s using that parameter. It forces anyone using that class to follow that form. It’s also possible to use self-bounding for generic methods:
```java
//: generics/SelfBoundingMethods.java
public class SelfBoundingMethods {
static <T extends SelfBounded<T>> T f(T arg) {
return arg.set(arg).get();
}
public static void main(String[] args) {
A a = f(new A());
}
} ///:~
```
This prevents the method from being applied to anything but a self-bounded argument of the form shown. Argument covariance The value of self-bounding types is that they produce covariant argument types—method argument types vary to follow the subclasses. Although self-bounding types also produce return types that are the same as the subclass type, this is not so important because covariant return types were introduced in Java SE5:
```java
//: generics/CovariantReturnTypes.java
class Base {}
class Derived extends Base {}
interface OrdinaryGetter {
Base get();
}
interface DerivedGetter extends OrdinaryGetter {
// Return type of overridden method is allowed to vary:
Derived get();
}
public class CovariantReturnTypes {
void test(DerivedGetter d) {
Derived d2 = d.get();
}
} ///:~
```

<!--p526-->
The get( ) method in DerivedGetter overrides get( ) in OrdinaryGetter and returns a type that is derived from the type returned by OrdinaryGetter.get( ). Although this is a Generics perfectly logical thing to do—a derived type method should be able to return a more specific type than the base type method that it’s overriding—it was illegal in earlier versions of Java. A self-bounded generic does in fact produce the exact derived type as a return value, as seen here with get( ):
```java
//: generics/GenericsAndReturnTypes.java
interface GenericGetter<T extends GenericGetter<T>> {
T get();
}
interface Getter extends GenericGetter<Getter> {}
public class GenericsAndReturnTypes {
void test(Getter g) {
Getter result = g.get();
GenericGetter gg = g.get(); // Also the base type
}
} ///:~
```
Notice that this code would not have compiled unless covariant return types were included in Java SE5. In non-generic code, however, the argument types cannot be made to vary with the subtypes:
```java
//: generics/OrdinaryArguments.java
class OrdinarySetter {
void set(Base base) {
System.out.println("OrdinarySetter.set(Base)");
}
}
class DerivedSetter extends OrdinarySetter {
void set(Derived derived) {
System.out.println("DerivedSetter.set(Derived)");
}
}
public class OrdinaryArguments {
public static void main(String[] args) {
Base base = new Base();
Derived derived = new Derived();
DerivedSetter ds = new DerivedSetter();
ds.set(derived);
ds.set(base); // Compiles: overloaded, not overridden!
}
} /* Output:
DerivedSetter.set(Derived)
OrdinarySetter.set(Base)
*///:~
```

<!--p527-->
Both set(derived) and set(base) are legal, so DerivedSetter.set( ) is not overriding OrdinarySetter.set( ), but instead it is overloading that method. From the output, you can see that there are two methods in DerivedSetter, so the base-class version is still available, thus verifying that it has been overloaded. However, with self-bounding types, there is only one method in the derived class, and that method takes the derived type as its argument, not the base type:
```java
//: generics/SelfBoundingAndCovariantArguments.java
interface SelfBoundSetter<T extends SelfBoundSetter<T>> {
void set(T arg);
}
interface Setter extends SelfBoundSetter<Setter> {}
public class SelfBoundingAndCovariantArguments {
void testA(Setter s1, Setter s2, SelfBoundSetter sbs) {
s1.set(s2);
// s1.set(sbs); // Error:
// set(Setter) in SelfBoundSetter<Setter>
// cannot be applied to (SelfBoundSetter)
}
} ///:~
```
The compiler doesn’t recognize the attempt to pass in the base type as an argument to set( ), because there is no method with that signature. The argument has, in effect, been overridden. Without self-bounding, the ordinary inheritance mechanism steps in, and you get overloading, just as with the non-generic case:
```java
//: generics/PlainGenericInheritance.java
class GenericSetter<T> { // Not self-bounded
void set(T arg){
System.out.println("GenericSetter.set(Base)");
}
}
class DerivedGS extends GenericSetter<Base> {
void set(Derived derived){
System.out.println("DerivedGS.set(Derived)");
}
}
public class PlainGenericInheritance {
public static void main(String[] args) {
Base base = new Base();
Derived derived = new Derived();
DerivedGS dgs = new DerivedGS();
dgs.set(derived);
dgs.set(base); // Compiles: overloaded, not overridden!
}
} /* Output:
DerivedGS.set(Derived)
GenericSetter.set(Base)
*///:~
```

<!--p528-->
This code mimics OrdinaryArguments.java; in that example, DerivedSetter inherits from OrdinarySetter which contains a set(Base). Here, DerivedGS inherits from GenericSetter<Base> which also contains a set(Base), created by the generic. And just like OrdinaryArguments.java, you can see from the output that DerivedGS contains two overloaded versions of set( ). Without self-bounding, you overload on argument types. If you use self-bounding, you only end up with one version of a method, which takes the exact argument type. Exercise 34: (4) Create a self-bounded generic type that contains an abstract method that takes an argument of the generic type parameter and produces a return value of the Generics generic type parameter. In a non-abstract method of the class, call the abstract method and return its result. Inherit from the self-bounded type and test the resulting class. Dynamic type safety Because you can pass generic containers to pre-Java SE5 code, there’s still the possibility that old-style code can corrupt your containers. Java SE5 has a set of utilities in java.util.Collections to solve the type-checking problem in this situation: the static methods checkedCollection( ), checkedList( ), checkedMap( ), checkedSet( ), checkedSortedMap( ) and checkedSortedSet( ). Each of these takes the container you want to dynamically check as the first argument and the type that you want to enforce as the second argument. A checked container will throw a ClassCastException at the point you try to insert an improper object, as opposed to a pre-generic (raw) container which would inform you that there was a problem when you pulled the object out. In the latter case, you know there’s a problem but you don’t know who the culprit is, but with checked containers you find out who tried to insert the bad object. Let’s look at the problem of "putting a cat in a list of dogs" using a checked container. Here, oldStyleMethod( ) represents legacy code because it takes a raw List, and the @SuppressWarnings("unchecked") annotation is necessary to suppress the resulting warning:
```java
//: generics/CheckedList.java
// Using Collection.checkedList().
import typeinfo.pets.*;
import java.util.*;
public class CheckedList {
@SuppressWarnings("unchecked")
static void oldStyleMethod(List probablyDogs) {
probablyDogs.add(new Cat());
}
public static void main(String[] args) {
List<Dog> dogs1 = new ArrayList<Dog>();
oldStyleMethod(dogs1); // Quietly accepts a Cat
List<Dog> dogs2 = Collections.checkedList(
new ArrayList<Dog>(), Dog.class);
try {
oldStyleMethod(dogs2); // Throws an exception
} catch(Exception e) {
System.out.println(e);
}
// Derived types work fine:
List<Pet> pets = Collections.checkedList(
new ArrayList<Pet>(), Pet.class);
pets.add(new Dog());
pets.add(new Cat());
}
} /* Output:
java.lang.ClassCastException: Attempt to insert class typeinfo.pets.Cat
element into collection with element type class typeinfo.pets.Dog
*///:~
```

<!--p529-->
When you run the program you’ll see that the insertion of a Cat goes unchallenged by dogs1, but dogs2 immediately throws an exception upon the insertion of an incorrect type. You can also see that it’s fine to put derived-type objects into a checked container that is checking for the base type. Exercise 35:(1) Modify CheckedList.java so that it uses the Coffee classes defined in this chapter. Exceptions Because of erasure, the use of generics with exceptions is extremely limited. A catch clause cannot catch an exception of a generic type, because the exact type of the exception must be known at both compile time and run time. Also, a generic class can’t directly or indirectly inherit from Throwable (this further prevents you from trying to define generic exceptions that can’t be caught). However, type parameters may be used in the throws clause of a method declaration. This allows you to write generic code that varies with the type of a checked exception:
```java
//: generics/ThrowGenericException.java
import java.util.*;
interface Processor<T,E extends Exception> {
void process(List<T> resultCollector) throws E;
}
class ProcessRunner<T,E extends Exception>
extends ArrayList<Processor<T,E>> {
List<T> processAll() throws E {
List<T> resultCollector = new ArrayList<T>();
for(Processor<T,E> processor : this)
processor.process(resultCollector);
return resultCollector;
}
}
class Failure1 extends Exception {}
class Processor1 implements Processor<String,Failure1> {
static int count = 3;
public void
process(List<String> resultCollector) throws Failure1 {
if(count-- > 1)
resultCollector.add("Hep!");
else
resultCollector.add("Ho!");
if(count < 0)
throw new Failure1();
}
}
class Failure2 extends Exception {}
class Processor2 implements Processor<Integer,Failure2> {
static int count = 2;
public void
process(List<Integer> resultCollector) throws Failure2 {
if(count-- == 0)
resultCollector.add(47);
else {
resultCollector.add(11);
}
if(count < 0)
throw new Failure2();
}
```

<!--p530-->
Generics
```java
}
public class ThrowGenericException {
public static void main(String[] args) {
ProcessRunner<String,Failure1> runner =
new ProcessRunner<String,Failure1>();
for(int i = 0; i < 3; i++)
runner.add(new Processor1());
try {
System.out.println(runner.processAll());
} catch(Failure1 e) {
System.out.println(e);
}
ProcessRunner<Integer,Failure2> runner2 =
new ProcessRunner<Integer,Failure2>();
for(int i = 0; i < 3; i++)
runner2.add(new Processor2());
try {
System.out.println(runner2.processAll());
} catch(Failure2 e) {
System.out.println(e);
}
}
} ///:~
```

<!--p531-->
A Processor performs a process( ) and may throw an exception of type E. The result of the process( ) is stored in the List<T> resultCollector (this is called a collecting parameter). A ProcessRunner has a processAll( ) method that executes every Process object that it holds, and returns the resultCollector. If you could not parameterize the exceptions that are thrown, you would be unable to write this code generically because of the checked exceptions. Exercise 36:(2) Add a second parameterized exception to the Processor class and demonstrate that the exceptions can vary independently. Mixins The term mixin seems to have acquired numerous meanings over time, but the fundamental concept is that of mixing in capabilities from multiple classes in order to produce a resulting class that represents all the types of the mixins. This is often something you do at the last minute, which makes it convenient to easily assemble classes. One value of mixins is that they consistently apply characteristics and behaviors across multiple classes. As a bonus, if you want to change something in a mixin class, those changes are then applied across all the classes where the mixin is applied. Because of this, mixins have part of the flavor of aspect-oriented programming (AOP), and aspects are often suggested to solve the mixin problem. Mixins in C++ One of the strongest arguments made for multiple inheritance in C++ is for the use of mixins. However, a more interesting and elegant approach to mixins is using parameterized types, whereby a mixin is a class that inherits from its type parameter. In C++, you can easily create mixins because C++ remembers the type of its template parameters. Here’s a C++ example with two mixin types: one that allows you to mix in the property of having a time stamp, and another that mixes in a serial number for each object instance:
```java
//: generics/Mixins.cpp
#include <string>
#include <ctime>
#include <iostream>
using namespace std;
template<class T> class TimeStamped : public T {
long timeStamp;
public:
TimeStamped() { timeStamp = time(0); }
long getStamp() { return timeStamp; }
};
template<class T> class SerialNumbered : public T {
long serialNumber;
static long counter;
public:
SerialNumbered() { serialNumber = counter++; }
long getSerialNumber() { return serialNumber; }
};
// Define and initialize the static storage:
template<class T> long SerialNumbered<T>::counter = 1;
class Basic {
string value;
public:
void set(string val) { value = val; }
string get() { return value; }
};
int main() {
TimeStamped<SerialNumbered<Basic> > mixin1, mixin2;
mixin1.set("test string 1");
mixin2.set("test string 2");
```

<!--p532-->
Generics
```java
cout << mixin1.get() << " " << mixin1.getStamp() <<
" " << mixin1.getSerialNumber() << endl;
cout << mixin2.get() << " " << mixin2.getStamp() <<
" " << mixin2.getSerialNumber() << endl;
} /* Output: (Sample)
test string 1 1129840250 1
test string 2 1129840250 2
*///:~
```
In main( ), the resulting type of mixin1 and mixin2 has all the methods of the mixed-in types. You can think of a mixin as a function that maps existing classes to new subclasses. Notice how trivial it is to create a mixin using this technique; basically, you just say, "Here’s what I want," and it happens:
```java
TimeStamped<SerialNumbered<Basic> > mixin1, mixin2;
```
Unfortunately, Java generics don’t permit this. Erasure forgets the base-class type, so a generic class cannot inherit directly from a generic parameter. Mixing with interfaces A commonly suggested solution is to use interfaces to produce the effect of mixins, like this:

<!--p533-->
```java
//: generics/Mixins.java
import java.util.*;
interface TimeStamped { long getStamp(); }
class TimeStampedImp implements TimeStamped {
private final long timeStamp;
public TimeStampedImp() {
timeStamp = new Date().getTime();
}
public long getStamp() { return timeStamp; }
}
interface SerialNumbered { long getSerialNumber(); }
class SerialNumberedImp implements SerialNumbered {
private static long counter = 1;
private final long serialNumber = counter++;
public long getSerialNumber() { return serialNumber; }
}
interface Basic {
public void set(String val);
public String get();
}
class BasicImp implements Basic {
private String value;
public void set(String val) { value = val; }
public String get() { return value; }
}
class Mixin extends BasicImp
implements TimeStamped, SerialNumbered {
private TimeStamped timeStamp = new TimeStampedImp();
private SerialNumbered serialNumber =
new SerialNumberedImp();
```
Generics
```java
public long getStamp() { return timeStamp.getStamp(); }
public long getSerialNumber() {
return serialNumber.getSerialNumber();
}
}
public class Mixins {
public static void main(String[] args) {
Mixin mixin1 = new Mixin(), mixin2 = new Mixin();
mixin1.set("test string 1");
mixin2.set("test string 2");
System.out.println(mixin1.get() + " " +
mixin1.getStamp() + " " + mixin1.getSerialNumber());
System.out.println(mixin2.get() + " " +
mixin2.getStamp() + " " + mixin2.getSerialNumber());
}
} /* Output: (Sample)
test string 1 1132437151359 1
test string 2 1132437151359 2
*///:~
```
The Mixin class is basically using delegation, so each mixed-in type requires a field in Mixin, and you must write all the necessary methods in Mixin toforward calls to the appropriate object. This example uses trivial classes, but with a more complex mixin the code grows rapidly.4 Exercise 37:(2) Add a new mixin class Colored to Mixins.java, mix it into Mixin, and show that it works. Using the Decorator pattern When you look at the way that it is used, the concept of a mixin seems closely related to the Decorator design pattern.5 Decorators are often used when, in order to satisfy every possible combination, simple subclassing produces so many classes that it becomes impractical. The Decorator pattern uses layered objects to dynamically and transparently add responsibilities to individual objects. Decorator specifies that all objects that wrap around your initial object have the same basic interface. Something is decoratable, and you layer on functionality by wrapping other classes around the decoratable. This makes the use of the decorators transparentthere are a set of common messages you can send to an object whether it has been decorated or not. A decorating class can also add methods, but as you shall see, this is limited. Decorators are implemented using composition and formal structures (the decoratable/decorator hierarchy), whereas mixins are inheritance-based. So you could think of parameterized-type-based mixins as a generic decorator mechanism that does not require the inheritance structure of the Decorator design pattern. The previous example can be recast using Decorator:
```java
//: generics/decorator/Decoration.java
package generics.decorator;
import java.util.*;
```

<!--p534-->
4Note that some programming environments, such as Eclipse and IntelliJ Idea, will automatically generate delegation code. 5Patterns are the subject of Thinking in Patterns (with Java), which you can find at www.MindView.net. See also Design Patterns, by Erich Gamma et al. (Addison-Wesley, 1995)-
```java
class Basic {
private String value;
public void set(String val) { value = val; }
public String get() { return value; }
}
class Decorator extends Basic {
protected Basic basic;
public Decorator(Basic basic) { this.basic = basic; }
public void set(String val) { basic.set(val); }
public String get() { return basic.get(); }
}
class TimeStamped extends Decorator {
private final long timeStamp;
public TimeStamped(Basic basic) {
super(basic);
timeStamp = new Date().getTime();
}
public long getStamp() { return timeStamp; }
}
class SerialNumbered extends Decorator {
private static long counter = 1;
private final long serialNumber = counter++;
public SerialNumbered(Basic basic) { super(basic); }
public long getSerialNumber() { return serialNumber; }
}
public class Decoration {
public static void main(String[] args) {
TimeStamped t = new TimeStamped(new Basic());
TimeStamped t2 = new TimeStamped(
new SerialNumbered(new Basic()));
//! t2.getSerialNumber(); // Not available
SerialNumbered s = new SerialNumbered(new Basic());
SerialNumbered s2 = new SerialNumbered(
new TimeStamped(new Basic()));
//! s2.getStamp(); // Not available
}
} ///:~
```

<!--p535-->
The class resulting from a mixin contains all the methods of interest, but the type of the object that results from using decorators is the last type that it was decorated with. That is, although it’s possible to add more than one layer, the final layer is the actual type, so only the final layer’s methods are visible, whereas the type of the mixin is all the types that have been mixed together. So a significant drawback to Decorator is that it only effectively works with one layer of decoration (the final one), and the mixin approach is arguably more natural. Thus, Decorator is only a limited solution to the problem addressed by mixins. Exercise 38:(4) Create a simple Decorator system by starting with basic coffee, then providing decorators of steamed milk, foam, chocolate, caramel and whipped cream. Mixins with dynamic proxies It’s possible to use a dynamic proxy to create a mechanism that more closely models mixins than does the Decorator (see the Type Information chapter for an explanation of how Java’s dynamic proxies work). With a dynamic proxy, the dynamic type of the resulting class is the combined types that have been mixed in. Because of the constraints of dynamic proxies, each class that is mixed in must be the implementation of an interface:
```java
//: generics/DynamicProxyMixin.java
import java.lang.reflect.*;
import java.util.*;
import net.mindview.util.*;
import static net.mindview.util.Tuple.*;
class MixinProxy implements InvocationHandler {
Map<String,Object> delegatesByMethod;
public MixinProxy(TwoTuple<Object,Class<?>>... pairs) {
delegatesByMethod = new HashMap<String,Object>();
for(TwoTuple<Object,Class<?>> pair : pairs) {
for(Method method : pair.second.getMethods()) {
String methodName = method.getName();
// The first interface in the map
// implements the method.
if (!delegatesByMethod.containsKey(methodName))
delegatesByMethod.put(methodName, pair.first);
}
}
}
public Object invoke(Object proxy, Method method,
Object[] args) throws Throwable {
String methodName = method.getName();
Object delegate = delegatesByMethod.get(methodName);
return method.invoke(delegate, args);
}
@SuppressWarnings("unchecked")
public static Object newInstance(TwoTuple... pairs) {
Class[] interfaces = new Class[pairs.length];
for(int i = 0; i < pairs.length; i++) {
interfaces[i] = (Class)pairs[i].second;
}
ClassLoader cl =
pairs[0].first.getClass().getClassLoader();
return Proxy.newProxyInstance(
cl, interfaces, new MixinProxy(pairs));
}
}
public class DynamicProxyMixin {
public static void main(String[] args) {
Object mixin = MixinProxy.newInstance(
tuple(new BasicImp(), Basic.class),
tuple(new TimeStampedImp(), TimeStamped.class),
tuple(new SerialNumberedImp(),SerialNumbered.class));
Basic b = (Basic)mixin;
TimeStamped t = (TimeStamped)mixin;
SerialNumbered s = (SerialNumbered)mixin;
b.set("Hello");
System.out.println(b.get());
System.out.println(t.getStamp());
System.out.println(s.getSerialNumber());
}
} /* Output: (Sample)
Hello
1132519137015
*///:~
```

<!--p536-->

<!--p537-->
Generics Because only the dynamic type, and not the static type, includes all the mixed-in types, this is still not quite as nice as the C++ approach, because you’re forced to downcast to the appropriate type before you can call methods for it. However, it is significantly closer to a true mixin. There has been a fair amount of work done towards the support of mixins for Java, including the creation of at least one language add-on, the Jam language, specifically for supporting mixins. Exercise 39:(1) Add a new mixin class Colored to DynamicProxyMixin.java, mix it into mixin, and show that it works. Latent typing The beginning of this chapter introduced the idea of writing code that can be applied as generally as possible. To do this, we need ways to loosen the constraints on the types that our code works with, without losing the benefits of static type checking. We are then able to write code that can be used in more situations without change—that is, more "generic" code. Java generics appear to take a further step in this direction. When you are writing or using generics that simply hold objects, the code works with any type (except for primitives, although as you’ve seen, autoboxing smoothes this over). Or, put another way, "holder" generics are able to say, "I don’t care what type you are." Code that doesn’t care what type it works with can indeed be applied everywhere, and is thus quite "generic." As you’ve also seen, a problem arises when you want to perform manipulations on generic types (other than calling Object methods), because erasure requires that you specify the bounds of the generic types that may be used, in order to safely call specific methods for the generic objects in your code. This is a significant limitation to the concept of "generic" because you must constrain your generic types so that they inherit from particular classes or implement particular interfaces. In some cases you might end up using an ordinary class or interface instead, because a bounded generic might be no different from specifying a class or interface. One solution that some programming languages provide is called latent typing or structural typing. A more whimsical term is duck typing, as in, "If it walks like a duck and talks like a duck, you might as well treat it like a duck." Duck typing has become a fairly popular term, possibly because it doesn’t carry the historical baggage that other terms do. Generic code typically only calls a few methods on a generic type, and a language with latent typing loosens the constraint (and produces more generic code) by only requiring that a subset of methods be implemented, not a particular class or interface. Because of this, latent typing allows you to cut across class hierarchies, calling methods that are not part of a common interface. So a piece of code might say, in effect, "I don’t care what type you are as long as you can speak( ) and sit( )." By not requiring a specific type, your code can be more generic. Latent typing is a code organization and reuse mechanism. With it you can write a piece of code that can be reused more easily than without it. Code organization and reuse are the foundational levers of all computer programming: Write it once, use it more than once, and keep the code in one place. Because I am not required to name an exact interface that my code operates upon, with latent typing I can write less code and apply it more easily in more places. Generics Two examples of languages that support latent typing are Python (freely downloadable from www.Python.org) and C++.6Python is a dynamically typed language (virtually all the type checking happens at run time) and C++ is a statically typed language (the type checking happens at compile time), so latent typing does not require either static or dynamic type checking. If we take the above description and express it in Python, it looks like this:
```java
#: generics/DogsAndRobots.py
class Dog:
def speak(self):
print "Arf!"
def sit(self):
print "Sitting"
def reproduce(self):
pass
class Robot:
def speak(self):
print "Click!"
def sit(self):
print "Clank!"
def oilChange(self) :
pass
def perform(anything):
anything.speak()
anything.sit()
a = Dog()
b = Robot()
perform(a)
perform(b)
#:~
```
Python uses indentation to determine scope (so no curly braces are needed), and a colon to begin a new scope. A ‘#’ indicates a comment to the end of the line, like ‘//’ in Java. The methods of a class explicitly specify the equivalent of the this reference as the first argument, called self by convention. Constructor calls do not require any sort of "new"keyword. And Python allows regular (non-member) functions, as evidenced by perform( ). In perform(anything), notice that there is no type for anything, and anything is just an identifier. It must be able to perform the operations that perform( ) asks of it, so an interface is implied. But you never have to explicitly write out that interface—it’s latent. perform( ) doesn’t care about the type of its argument, so I can pass any object to it as long as it supports the speak( ) and sit( ) methods. If you pass an object to perform( ) that does not support these operations, you’ll get a runtime exception. We can produce the same effect in C++:
```java
//: generics/DogsAndRobots.cpp
class Dog {
public:
void speak() {}
void sit() {}
void reproduce() {}
```

<!--p538-->
6The Ruby and Smalltalk languages also support latent typing.
```java
};
class Robot {
public:
void speak() {}
void sit() {}
void oilChange() {
};
template<class T> void perform(T anything) {
anything.speak();
anything.sit();
}
int main() {
Dog d;
Robot r;
perform(d);
perform(r);
} ///:~
```
In both Python and C++, Dog and Robot have nothing in common, other than that they happen to have two methods with identical signatures. From a type standpoint, they are completely distinct types. However, perform( ) doesn’t care about the specific type of its argument, and latent typing allows it to accept both types of object. C++ ensures that it can actually send those messages. The compiler gives you an error message if you try to pass the wrong type (these error messages have historically been terrible and verbose, and are the primary reason that C++ templates have a poor reputation). Although they do it at different times— C++ at compile time, and Python at run time—both languages ensure that types cannot be misused and are thus considered to be strongly typed.7Latent typing does not compromise strong typing. Because generics were added to Java late in the game, there was no chance that any kind of latent typing could be implemented, so Java has no support for this feature. As a result, it initially seems that Java’s generic mechanism is "less generic" than a language that supports latent typing.8For instance, if we try to implement the above example in Java, we are forced to use a class or an interface and specify it in a bounds expression:
```java
//: generics/Performs.java
public interface Performs {
void speak();
void sit();
} ///:~
//: generics/DogsAndRobots.java
// No latent typing in Java
import typeinfo.pets.*;
import static net.mindview.util.Print.*;
class PerformingDog extends Dog implements Performs {
public void speak() { print("Woof!"); }
public void sit() { print("Sitting"); }
public void reproduce() {}
}
```

<!--p539-->
7 Because you can use casts, which effectively disable the type system, some people argue that C++ is weakly typed, but that’s extreme. It’s probably safer to say that C++ is "strongly typed with a trap door." 8 The implementation of Java’s generics using erasure is sometimes referred to as secondclass generic types.
```java
class Robot implements Performs {
public void speak() { print("Click!"); }
public void sit() { print("Clank!"); }
public void oilChange() {}
}
class Communicate {
public static <T extends Performs>
void perform(T performer) {
performer.speak();
performer.sit();
}
}
public class DogsAndRobots {
public static void main(String[] args) {
PerformingDog d = new PerformingDog();
Robot r = new Robot();
Communicate.perform(d);
Communicate.perform(r);
}
} /* Output:
Woof!
Sitting
Click!
Clank!
*///:~
```
However, note that perform( ) does not need to use generics in order to work. It can simply be specified to accept a Performs object:
```java
//: generics/SimpleDogsAndRobots.java
// Removing the generic; code still works.
class CommunicateSimply {
static void perform(Performs performer) {
performer.speak();
performer.sit();
}
}
public class SimpleDogsAndRobots {
public static void main(String[] args) {
CommunicateSimply.perform(new PerformingDog());
CommunicateSimply.perform(new Robot());
}
} /* Output:
Woof!
Sitting
Click!
Clank!
*///:~
```

<!--p540-->
In this case, generics were simply not necessary, since the classes were already forced to implement the Performs interface. Generics Compensating for the lack of latent typing Although Java does not support latent typing, it turns out that this does not mean that your bounded generic code cannot be applied across different type hierarchies. That is, it is still possible to create truly generic code, but it takes some extra effort. Reflection One approach you can use is reflection. Here’s a perform( ) method that uses latent typing:

<!--p541-->
```java
//: generics/LatentReflection.java
// Using Reflection to produce latent typing.
import java.lang.reflect.*;
import static net.mindview.util.Print.*;
// Does not implement Performs:
class Mime {
public void walkAgainstTheWind() {}
public void sit() { print("Pretending to sit"); }
public void pushInvisibleWalls() {}
public String toString() { return "Mime"; }
}
// Does not implement Performs:
class SmartDog {
public void speak() { print("Woof!"); }
public void sit() { print("Sitting"); }
public void reproduce() {}
}
class CommunicateReflectively {
public static void perform(Object speaker) {
Class<?> spkr = speaker.getClass();
try {
try {
Method speak = spkr.getMethod("speak");
speak.invoke(speaker);
} catch(NoSuchMethodException e) {
print(speaker + " cannot speak");
}
try {
Method sit = spkr.getMethod("sit");
sit.invoke(speaker);
} catch(NoSuchMethodException e) {
print(speaker + " cannot sit");
}
} catch(Exception e) {
throw new RuntimeException(speaker.toString(), e);
}
}
}
public class LatentReflection {
public static void main(String[] args) {
CommunicateReflectively.perform(new SmartDog());
CommunicateReflectively.perform(new Robot());
CommunicateReflectively.perform(new Mime());
}
} /* Output:
Woof!
Sitting
Click!
Clank!
Mime cannot speak
Pretending to sit
*///:~
```
Here, the classes are completely disjoint and have no base classes (other than Object) or interfaces in common. Through reflection, CommunicateReflectively.perform( ) is able to dynamically establish whether the desired methods are available and call them. It is even able to deal with the fact that Mime only has one of the necessary methods, and partially fulfills its goal. Applying a method to a sequence Reflection provides some interesting possibilities, but it relegates all the type checking to run time, and is thus undesirable in many situations. If you can achieve compile-time type checking, that’s usually more desirable. But is it possible to have compile-time type checking and latent typing? Let’s look at an example that explores the problem. Suppose you want to create an apply( ) method that will apply any method to every object in a sequence. This is a situation where interfaces don’t seem to fit. You want to apply any method to a collection of objects, and interfaces constrain you too much to describe "any method." How do you do this in Java? Initially, we can solve the problem with reflection, which turns out to be fairly elegant because of Java SE5 varargs:
```java
//: generics/Apply.java
// {main: ApplyTest}
import java.lang.reflect.*;
import java.util.*;
import static net.mindview.util.Print.*;
public class Apply {
public static <T, S extends Iterable<? extends T>>
void apply(S seq, Method f, Object... args) {
try {
for(T t: seq)
f.invoke(t, args);
} catch(Exception e) {
// Failures are programmer errors
throw new RuntimeException(e);
}
}
}
class Shape {
public void rotate() { print(this + " rotate"); }
public void resize(int newSize) {
print(this + " resize " + newSize);
}
}
class Square extends Shape {}
class FilledList<T> extends ArrayList<T> {
```

<!--p542-->
Generics
```java
public FilledList(Class<? extends T> type, int size) {
try {
for(int i = 0; i < size; i++)
// Assumes default constructor:
add(type.newInstance());
} catch(Exception e) {
throw new RuntimeException(e);
}
}
}
class ApplyTest {
public static void main(String[] args) throws Exception {
List<Shape> shapes = new ArrayList<Shape>();
for(int i = 0; i < 10; i++)
shapes.add(new Shape());
Apply.apply(shapes, Shape.class.getMethod("rotate"));
Apply.apply(shapes,
Shape.class.getMethod("resize", int.class), 5);
List<Square> squares = new ArrayList<Square>();
for(int i = 0; i < 10; i++)
squares.add(new Square());
Apply.apply(squares, Shape.class.getMethod("rotate"));
Apply.apply(squares,
Shape.class.getMethod("resize", int.class), 5);
Apply.apply(new FilledList<Shape>(Shape.class, 10),
Shape.class.getMethod("rotate"));
Apply.apply(new FilledList<Shape>(Square.class, 10),
Shape.class.getMethod("rotate"));
SimpleQueue<Shape> shapeQ = new SimpleQueue<Shape>();
for(int i = 0; i < 5; i++) {
shapeQ.add(new Shape());
shapeQ.add(new Square());
}
Apply.apply(shapeQ, Shape.class.getMethod("rotate"));
}
} /* (Execute to see output) *///:~
```
In Apply, we get lucky because there happens to be an Iterable interface built into Java which is used by the Java containers library. Because of this, the apply( ) method can accept anything that implements the Iterable interface, which includes all the Collection classes such as List. But it can also accept anything else, as long as you make it Iterable—for example, the SimpleQueue class defined here and used above in main( ):
```java
//: generics/SimpleQueue.java
// A different kind of container that is Iterable
import java.util.*;
public class SimpleQueue<T> implements Iterable<T> {
private LinkedList<T> storage = new LinkedList<T>();
public void add(T t) { storage.offer(t); }
public T get() { return storage.poll(); }
public Iterator<T> iterator() {
return storage.iterator();
}
} ///:~
```

<!--p543-->
In Apply.java, exceptions are converted to RuntimeExceptions because there’s not much of a way to recover from exceptions—they really do represent programmer errors in this case. Generics Note that I had to put in bounds and wildcards in order for Apply and FilledList to be used in all desired situations. You can experiment by taking these out, and you’ll discover that some applications of Apply and FilledList will not work. FilledList presents a bit of a quandary. In order for a type to be used, it must have a default (no-arg) constructor. Java has no way to assert such a thing at compile time, so it becomes a runtime issue. A common suggestion to ensure compile-time checking is to define a factory interface that has a method that generates objects; then FilledList would accept that interface rather than the "raw factory" of the type token. The problem with this is that all the classes you use in FilledList must then implement your factory interface. Alas, most classes are created without knowledge of your interface, and therefore do not implement it. Later, I’ll show one solution using adapters. But the approach shown, of using a type token, is perhaps a reasonable tradeoff (at least as a first-cut solution). With this approach, using something like FilledList is just easy enough that it may be used rather than ignored. Of course, because errors are reported at run time, you need confidence that these errors will appear early in the development process. Note that the type token technique is recommended in the Java literature, such as Gilad Bracha’s paper Generics in the Java Programming Language,9where he notes, "It’s an idiom that’s used extensively in the new APIs for manipulating annotations, for example." However, I’ve discovered some inconsistency in people’s comfort level with this technique; some people strongly prefer the factory approach, which was presented earlier in this chapter. Also, as elegant as the Java solution turns out to be, we must observe that the use of reflection (although it has been improved significantly in recent versions of Java) may be slower than a non-reflection implementation, since so much is happening at run time. This should not stop you from using the solution, at least as a first cut (lest you fall sway to premature optimization), but it’s certainly a distinction between the two approaches. Exercise 40:(3)Add a speak( ) method to all the pets in typeinfo.pets. Modify Apply.java to call the speak( ) method for a heterogeneous collection of Pet. When you don’t happen to have the right interface The above example benefited because the Iterable interface was already built in, and was exactly what we needed. But what about the general case, when there isn’t an interface already in place that just happens to fit your needs? For example, let’s generalize the idea in FilledList and create a parameterized fill( ) method that will take a sequence and fill it using a Generator. When we try to write this in Java, we run into a problem, because there is no convenient "Addable"interface as there was an Iterable interface in the previous example. So instead of saying, "anything that you can call add( ) for," you must say, "subtype of Collection."The resulting code is not particularly generic, since it must be constrained to work with Collection implementations. If I try to use a class that doesn’t implement Collection, my generic code won’t work. Here’s what it looks like:
```java
//: generics/Fill.java
// Generalizing the FilledList idea
// {main: FillTest}
import java.util.*;
```

<!--p544-->
9 See citation at the end of this chapter.
```java
// Doesn’t work with "anything that has an add()." There is
// no "Addable" interface so we are narrowed to using a
// Collection. We cannot generalize using generics in
// this case.
public class Fill {
public static <T> void fill(Collection<T> collection,
Class<? extends T> classToken, int size) {
for(int i = 0; i < size; i++)
// Assumes default constructor:
try {
collection.add(classToken.newInstance());
} catch(Exception e) {
throw new RuntimeException(e);
}
}
}
class Contract {
private static long counter = 0;
private final long id = counter++;
public String toString() {
return getClass().getName() + " " + id;
}
}
class TitleTransfer extends Contract {}
class FillTest {
public static void main(String[] args) {
List<Contract> contracts = new ArrayList<Contract>();
Fill.fill(contracts, Contract.class, 3);
Fill.fill(contracts, TitleTransfer.class, 2);
for(Contract c: contracts)
System.out.println(c);
SimpleQueue<Contract> contractQueue =
new SimpleQueue<Contract>();
// Won’t work. fill() is not generic enough:
// Fill.fill(contractQueue, Contract.class, 3);
}
} /* Output:
Contract 0
Contract 1
Contract 2
TitleTransfer 3
TitleTransfer 4
*///:~
```

<!--p545-->
This is where a parameterized type mechanism with latent typing is valuable, because you are not at the mercy of the past design decisions of any particular library creator, so you do not have to rewrite your code every time you encounter a new library that didn’t take your situation into account (thus the code is truly "generic"). In the above case, because the Java designers (understandably) did not see the need for an "Addable" interface, we are constrained within the Collection hierarchy, and SimpleQueue, even though it has an add( ) method, will not work. Because it is thus constrained to working with Collection, the code is not particularly "generic." With latent typing, this would not be the case. Simulating latent typing with adapters So Java generics don’t have latent typing, and we need something like latent typing in order to write code that can be applied across class boundaries (that is, "generic" code). Is there some way to get around this limitation? What would latent typing accomplish here? It means that you could write code saying, "I don’t care what type I’m using here as long as it has these methods." In effect, latent typing creates an implicit interface containing the desired methods. So it follows that if we write the necessary interface by hand (since Java doesn’t do it for us), that should solve the problem. Writing code to produce an interface that we want from an interface that we have is an example of the Adapter design pattern. We can use adapters to adapt existing classes to produce the desired interface, with a relatively small amount of code. The solution, which uses the previously defined Coffee hierarchy, demonstrates different ways of writing adapters:
```java
//: generics/Fill2.java
// Using adapters to simulate latent typing.
// {main: Fill2Test}
import generics.coffee.*;
import java.util.*;
import net.mindview.util.*;
import static net.mindview.util.Print.*;
interface Addable<T> { void add(T t); }
public class Fill2 {
// Classtoken version:
public static <T> void fill(Addable<T> addable,
Class<? extends T> classToken, int size) {
for(int i = 0; i < size; i++)
try {
addable.add(classToken.newInstance());
} catch(Exception e) {
throw new RuntimeException(e);
}
}
// Generator version:
public static <T> void fill(Addable<T> addable,
Generator<T> generator, int size) {
for(int i = 0; i < size; i++)
addable.add(generator.next());
}
}
// To adapt a base type, you must use composition.
// Make any Collection Addable using composition:
class AddableCollectionAdapter<T> implements Addable<T> {
private Collection<T> c;
public AddableCollectionAdapter(Collection<T> c) {
this.c = c;
}
public void add(T item) { c.add(item); }
}
// A Helper to capture the type automatically:
class Adapter {
public static <T>
Addable<T> collectionAdapter(Collection<T> c) {
return new AddableCollectionAdapter<T>(c);
}
```

<!--p546-->
Generics
```java
}
// To adapt a specific type, you can use inheritance.
// Make a SimpleQueue Addable using inheritance:
class AddableSimpleQueue<T>
extends SimpleQueue<T> implements Addable<T> {
public void add(T item) { super.add(item); }
}
class Fill2Test {
public static void main(String[] args) {
// Adapt a Collection:
List<Coffee> carrier = new ArrayList<Coffee>();
Fill2.fill(
new AddableCollectionAdapter<Coffee>(carrier),
Coffee.class, 3);
// Helper method captures the type:
Fill2.fill(Adapter.collectionAdapter(carrier),
Latte.class, 2);
for(Coffee c: carrier)
print(c);
print("----------------------");
// Use an adapted class:
AddableSimpleQueue<Coffee> coffeeQueue =
new AddableSimpleQueue<Coffee>();
Fill2.fill(coffeeQueue, Mocha.class, 4);
Fill2.fill(coffeeQueue, Latte.class, 1);
for(Coffee c: coffeeQueue)
print(c);
}
} /* Output:
Coffee 0
Coffee 1
Coffee 2
Latte 3
Latte 4
----------------------
Mocha 5
Mocha 6
Mocha 7
Mocha 8
Latte 9
*///:~
```

<!--p547-->

<!--p548-->
Fill2 doesn’t require a Collection as Fill did. Instead, it only needs something that implements Addable, and Addable has been written just for Fill—it is a manifestation of the latent type that I wanted the compiler to make for me. In this version, I’ve also added an overloaded fill( ) that takes a Generator rather than a type token. The Generator is type-safe at compile time: The compiler ensures that you pass it a proper Generator, so no exceptions can be thrown. The first adapter, AddableCollectionAdapter, works with the base type Collection, which means that any implementation of Collection can be used. This version simply stores the Collection reference and uses it to implement add( ). If you have a specific type rather than the base class of a hierarchy, you can write somewhat less code when creating your adapter by using inheritance, as you can see in AddableSimpleQueue. In Fill2Test.main( ), you can see the various types of adapters at work. First, a Collection type is adapted with AddableCollectionAdapter. A second version of this uses a generic helper method, and you can see how the generic method captures the type so it doesn’t have to be explicitly written— this is a convenient trick that produces more elegant code. Next, the pre-adapted AddableSimpleQueue is used. Note that in both cases the adapters allow the classes that previously didn’t implement Addable to be used with Fill2.fill( ). Using adapters like this would seem to compensate for the lack of latent typing, and thus allow you to write genuinely generic code. However, it’s an extra step and something that must be understood both by the library creator and the library consumer, and the concept may not be grasped as readily by less experienced programmers. By removing the extra step, latent typing makes generic code easier to apply, and this is its value. Exercise 41:(1) Modify Fill2.java to use the classes in typeinfo.pets instead of the Coffee classes. Generics Using function objects as strategies This final example will create truly generic code using the adapter approach described in the previous section. The example began as an attempt to create a sum over a sequence of elements (of any type that can be summed), but evolved into performing general operations using afunctional style of programming. If you just look at the process of trying to add objects, you can see that this is a case where we have common operations across classes, but the operations are not represented in any base class that we can specify—sometimes you can even use a’+’ operator, and other times there may be some kind of "add" method. This is generally the situation that you encounter when trying to write generic code, because you want the code to apply across multiple classes— especially, as in this case, multiple classes that already exist and that we have no ability to "fix." Even if you were to narrow this case to subclasses of Number, that superclass doesn’t include anything about "addability." The solution is to use the Strategy design pattern, which produces more elegant code because it completely isolates "the thing that changes" inside of a function object.10A function object is an object that in some way behaves like a function—typically, there’s one method of interest (in languages that support operator overloading, you can make the call to this method look like an ordinary method call). The value of function objects is that, unlike an ordinary method, they can be passed around, and they can also have state that persists across calls. Of course, you can accomplish something like this with any method in a class, but (as with any design pattern) the function object is primarily distinguished by its intent. Here the intent is to create something that behaves like a single method that you can pass around; thus it is closely coupled with—and sometimes indistinguishable from—the Strategy design pattern. As I’ve found with a number of design patterns, the lines get kind of blurry here: We are creating function objects which perform adaptation, and they are being passed into methods to be used as strategies. Taking this approach, I added the various kinds of generic methods that I had originally set out to create, and more. Here is the result:
```java
//: generics/Functional.java
import java.math.*;
import java.util.concurrent.atomic.*;
import java.util.*;
import static net.mindview.util.Print.*;
// Different types of function objects:
interface Combiner<T> { T combine(T x, T y); }
interface UnaryFunction<R,T> { R function(T x); }
interface Collector<T> extends UnaryFunction<T,T> {
T result(); // Extract result of collecting parameter
}
interface UnaryPredicate<T> { boolean test(T x); }
public class Functional {
// Calls the Combiner object on each element to combine
// it with a running result, which is finally returned:
public static <T> T
```

<!--p549-->
10 You will sometimes see these called functors. I will use the term function object rather than^unctor, as the term "functor" has a specific and different meaning in mathematics.
```java
reduce(Iterable<T> seq, Combiner<T> combiner) {
Iterator<T> it = seq.iterator();
if(it.hasNext()) {
T result = it.next();
while(it.hasNext())
result = combiner.combine(result, it.next());
return result;
}
// If seq is the empty list:
return null; // Or throw exception
}
// Take a function object and call it on each object in
// the list, ignoring the return value. The function
// object may act as a collecting parameter, so it is
// returned at the end.
public static <T> Collector<T>
forEach(Iterable<T> seq, Collector<T> func) {
for(T t : seq)
func.function(t);
return func;
}
// Creates a list of results by calling a
// function object for each object in the list:
public static <R,T> List<R>
transform(Iterable<T> seq, UnaryFunction<R,T> func) {
List<R> result = new ArrayList<R>();
for(T t : seq)
result.add(func.function(t));
return result;
}
// Applies a unary predicate to each item in a sequence,
// and returns a list of items that produced "true":
public static <T> List<T>
filter(Iterable<T> seq, UnaryPredicate<T> pred) {
List<T> result = new ArrayList<T>();
for(T t : seq)
if(pred.test(t))
result.add(t);
return result;
}
// To use the above generic methods, we need to create
// function objects to adapt to our particular needs:
static class IntegerAdder implements Combiner<Integer> {
public Integer combine(Integer x, Integer y) {
return x + y;
}
}
static class
IntegerSubtracter implements Combiner<Integer> {
public Integer combine(Integer x, Integer y) {
return x - y;
}
}
static class
BigDecimalAdder implements Combiner<BigDecimal> {
public BigDecimal combine(BigDecimal x, BigDecimal y) {
return x.add(y);
}
}
static class
BigIntegerAdder implements Combiner<BigInteger> {
public BigInteger combine(BigInteger x, BigInteger y) {
return x.add(y);
```

<!--p550-->
Generics

<!--p551-->
```java
}
}
static class
AtomicLongAdder implements Combiner<AtomicLong> {
public AtomicLong combine(AtomicLong x, AtomicLong y) {
// Not clear whether this is meaningful:
return new AtomicLong(x.addAndGet(y.get()));
}
}
// We can even make a UnaryFunction with an "ulp"
// (Units in the last place):
static class BigDecimalUlp
implements UnaryFunction<BigDecimal,BigDecimal> {
public BigDecimal function(BigDecimal x) {
return x.ulp();
}
}
static class GreaterThan<T extends Comparable<T>>
implements UnaryPredicate<T> {
private T bound;
public GreaterThan(T bound) { this.bound = bound; }
public boolean test(T x) {
return x.compareTo(bound) > 0;
}
}
static class MultiplyingIntegerCollector
implements Collector<Integer> {
private Integer val = 1;
public Integer function(Integer x) {
val *= x;
return val;
}
public Integer result() { return val; }
}
public static void main(String[] args) {
// Generics, varargs & boxing working together:
List<Integer> li = Arrays.asList(1, 2, 3, 4, 5, 6, 7);
Integer result = reduce(li, new IntegerAdder());
print(result);
result = reduce(li, new IntegerSubtracter());
print(result);
print(filter(li, new GreaterThan<Integer>(4)));
print(forEach(li,
new MultiplyingIntegerCollector()).result());
print(forEach(filter(li, new GreaterThan<Integer>(4)),
new MultiplyingIntegerCollector()).result());
MathContext mc = new MathContext(7);
List<BigDecimal> lbd = Arrays.asList(
new BigDecimal(1.1, mc), new BigDecimal(2.2, mc),
new BigDecimal(3.3, mc), new BigDecimal(4.4, mc));
BigDecimal rbd = reduce(lbd, new BigDecimalAdder());
print(rbd);
print(filter(lbd,
new GreaterThan<BigDecimal>(new BigDecimal(3))));
// Use the prime-generation facility of BigInteger:
List<BigInteger> lbi = new ArrayList<BigInteger>();
BigInteger bi = BigInteger.valueOf(11);
for(int i = 0; i < 11; i++) {
lbi.add(bi);
bi = bi.nextProbablePrime();
}
print(lbi);
BigInteger rbi = reduce(lbi, new BigIntegerAdder());
print(rbi);
// The sum of this list of primes is also prime:
print(rbi.isProbablePrime(5));
List<AtomicLong> lal = Arrays.asList(
new AtomicLong(11), new AtomicLong(47),
new AtomicLong(74), new AtomicLong(133));
AtomicLong ral = reduce(lal, new AtomicLongAdder());
print(ral);
print(transform(lbd,new BigDecimalUlp()));
}
} /* Output:
-26
[5, 6, 7]
11.000000
[3.300000, 4.400000]
[11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
true
[0.000001, 0.000001, 0.000001, 0.000001]
*///:~
```

<!--p552-->
I begin by defining interfaces for different types of function objects. These were created on demand, as I developed the different methods and discovered the need for each. The Combiner class was suggested by an anonymous contributor to one of the articles posted on my Web site. The Combiner abstracts away the specific detail of trying to add two objects, and just says that they are being combined somehow. As a result, you can see that IntegerAdder and IntegerSubtracter can be types of Combiner. A UnaryFunction takes a single argument and produces a result; the argument and result need not be of the same type. A Collector is used as a "collecting parameter," and you can extract the result when you’re finished. A UnaryPredicate produces a boolean result. There are other types of function objects that can be defined, but these are enough to make the point. The Functional class contains a number of generic methods that apply function objects to sequences. reduce( ) applies the function in a Combiner to each element of a sequence in order to produce a single result. forEach( ) takes a Collector and applies its function to each element, ignoring the result of each function call. This can be called just for the side effect (which wouldn’t be a "functional" style of programming but can still be useful), or the Collector can maintain internal state to become a collecting parameter, as is the case in this example. transform( ) produces a list by calling a UnaryFunction on each object in the sequence and capturing the result. Generics Finally, filter( ) applies a UnaryPredicate to each object in a sequence and stores the ones that produce true in a List, which it returns. You can define additional generic functions. The C++ STL, for example, has lots of them. The problem has also been solved in some open-source libraries, such as the JGA (Generic Algorithms for Java). In C++, latent typing takes care of matching up operations when you call functions, but in Java we need to write the function objects to adapt the generic methods to our particular needs. So the next part of the class shows various different implementations of the function objects. Note, for example, that IntegerAdder and BigDecimalAdder solve the same problemadding two objects—by calling the appropriate operations for their particular type. So that’s the Adapter pattern and Strategy pattern combined. In main( ), you can see that in each method call, a sequence is passed along with the appropriate function object. Also, a number of the expressions can get fairly complex, such as:
```java
forEach(filter(li, new GreaterThan(4)),
new MultiplyingIntegerCollector()).result()
```

<!--p553-->

<!--p554-->

<!--p555-->
This produces a list by selecting all elements in li that are greater than 4, and then applies the MultiplyingIntegerCollector( ) to the resulting list and extracts the result( ). I won’t explain the details of the rest of the code other than to say that you can probably figure it out by walking through it. Exercise 42:(5) Create two separate classes, with nothing in common. Each class should hold a value, and at least have methods that produce that value and perform a modification upon that value. Modify Functional.java so that it performs functional operations on collections of your classes (these operations do not have to be arithmetic as they are in Functional.java). Summary: Is casting really so bad? Having worked to explain C++ templates since their inception, I have probably been putting forward the following argument longer than most people. Only recently have I stopped to wonder how often this argument is valid—how many times does the problem I’m about to describe really slip through the cracks? The argument goes like this. One of the most compelling places to use a generic type mechanism is with container classes such as the Lists, Sets, Maps, etc. that you saw in Holding Your Objects and that you shall see more of in the Containers in Depth chapter. Before Java SE5, when you put an object into a container, it would be upcast to Object, so you’d lose the type information. When you wanted to pull it back out to do something with it, you had to cast it back down to the proper type. My example was a List of Cat (a variation of this using apples and oranges is shown at the beginning of the Holding Your Objects chapter). Without the Java SE5 generic version of the container, you put Objects in and you get Objects out, so it’s easily possible to put a Dog in a List of Cat. However, pre-generic Java wouldn’t let you misuse the objects that you put into a container. If you threw a Dog into a container of Cats and then tried to treat everything in the container as a Cat, you’d get a RuntimeException when you pulled the Dog reference out of the Cat container and tried to cast it to a Cat. You’d still discover the problem, but you discovered it at run time rather than compile time. In previous editions of this book, I go on to say: This is more than just an annoyance. It’s something that can create difficult-to-find bugs. If one part (or several parts) of a program inserts objects into a container, and you discover only in a separate part of the program through an exception that a bad object was placed in the container, then you must find out where the bad insert occurred. However, upon further examination of the argument, I began to wonder about it. First, how often does it happen? I don’t remember this kind of thing ever happening to me, and when I asked people at conferences, I didn’t hear anyone say that it had happened to them. Another book used an example of a list called files that contained String objects—in this example it seemed perfectly natural to add a File object to files, so a better name for the object might have been fileNames. No matter how much type checking Java provides, it’s still possible to write obscure programs, and a badly written program that compiles is still a badly written program. Perhaps most people use well-named containers such as "cats" that provide a visual warning to the programmer who would try to add a non-Cat. And even if it did happen, how long would such a thing really stay buried? It would seem that as soon as you started running tests with real data, you’d see an exception pretty quickly. One author even asserted that such a bug could "remain buried for years." But I do not recall any deluge of reports of people having great difficulty finding "dog in cat list" bugs, or even producing them very often. Whereas you will see in the Concurrency chapter that with threads, it is very easy and common to have bugs that may appear extremely rarely, and only give you a vague idea of what’s wrong. So is the "dog in cat list" argument really the reason that this very significant and fairly complex feature has been added to Java? I believe the intent of the general-purpose language feature called "generics" (not necessarily Java’s particular implementation of it) is expressiveness, not just creating type-safe containers. Type-safe containers come as a side effect of the ability to create more general- purpose code. Generics So even though the "dog in cat list" argument is often used to justify generics, it is questionable. And as I asserted at the beginning of the chapter, I do not believe that this is what the concept of generics is really about. Instead, generics are as their name implies—a way to write more "generic" code that is less constrained by the types it can work with, so a single piece of code can be applied to more types. As you have seen in this chapter, it is fairly easy to write truly generic "holder" classes (which the Java containers are), but to write generic code that manipulates its generic types requires extra effort, on the part of both the class creator and the class consumer, who must understand the concept and implementation of the Adapter design pattern. That extra effort reduces the ease of use of the feature, and may thus make it less applicable in places where it might otherwise have added value. Also note that because generics were back-engineered into Java instead of being designed into the language from the start, some of the containers cannot be made as robust as they should be. For example, look at Map, in particular the methods containsKey(Object key) and get(Object key). If these classes had been designed with pre-existing generics, these methods would have used parameterized types instead of Object, thus affording the compile-time checking that generics are supposed to provide. In C++ maps, for example, the key type is always checked at compile time. One thing is very clear: Introducing any kind of generic mechanism in a later version of a language, after that language has come into general use, is a very, very messy proposition, and one that cannot be accomplished without pain. In C++, templates were introduced in the initial ISO version of the language (although even that caused some pain because there was an earlier nontemplate version in use before the first Standard C++ appeared), so in effect templates were always a part of the language. In Java, generics were not introduced until almost 10 years after the language was first released, so the issues of migrating to generics are quite considerable, and have made a significant impact on the design of generics. The result is that you, the programmer, will suffer because of the lack of vision exhibited by the Java designers when they created version l.o. When Java was first being created, the designers, of course, knew about C++ templates, and they even considered including them in the language, but for one reason or another decided to leave them out (indications are that they were in a hurry). As a result, both the language and the programmers that use it will suffer. Only time will show the ultimate impact that Java’s approach to generics will have on the language. Some languages, notably Nice (see http://nice.sourceforge.net; this language generates Java bytecodes and works with existing Java libraries) and NextGen (see http://japan.cs.rice.edu/nextgen) have incorporated cleaner and less impactful approaches to parameterized types. It’s not impossible to imagine such a language becoming a successor to Java, because it takes exactly the approach that C++ did with C: Use what’s there and improve upon it. Generics Further reading The introductory document for generics is Generics in the Java Programming Language, by Gilad Bracha, located at http://java.sun.eom/j2se/1.5/pdf/generics-tutorial.pdf Angelika Langer’s Java Generics FAQs is a very helpful resource, located at www.angelikalanger.com/GenericsFAQ/JavaGenericsFAQ.html. You can find out more about wildcards in Adding Wildcards to the Java Programming Language, by Torgerson, Ernst, Hansen, von der Ahe, Bracha and Gafter, located at www.jot.fm/issues/issue_2004_12/article5. Solutions to selected exercises can be found in the electronic document The Thinking in Java Annotated Solution Guide, available for sale from www.MindView.net.