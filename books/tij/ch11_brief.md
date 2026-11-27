# 11. Holding Your Objects (printed p275-312)


<!--p297-->
Holding Your Objects It’s a fairly simple program that only has a fixed quantity of objects with known lifetimes. In general, your programs will always be creating new objects based on some criteria that will be known only at run time. Before then, you won’t know the quantity or even the exact type of the objects you need. To solve the general programming problem, you need to create any number of objects, anytime, anywhere. So you can’t rely on creating a named reference to hold each one of your objects:
```java
MyType aReference;
```

<!--p298-->
since you’ll never know how many of these you’ll actually need. Most languages provide some way to solve this essential problem. Java has several ways to hold objects (or rather, references to objects). The compiler-supported type is the array, which has been discussed before. An array is the most efficient way to hold a group of objects, and you’re pointed towards this choice if you want to hold a group of primitives. But an array has a fixed size, and in the more general case, you won’t know at the time you’re writing the program how many objects you’re going to need, or whether you need a more sophisticated way to store your objects—so the fixed-sized constraint of an array is too limiting. The java.util library has a reasonably complete set of container classes to solve this problem, the basic types of which are List, Set, Queue, and Map. These types of objects are also known as collection classes, but because the Java library uses the name Collection to refer to a particular subset of the library, I shall use the more inclusive term "container." Containers provide sophisticated ways to hold your objects, and you can solve a surprising number of problems by using these tools. Among their other characteristics—Set, for example, holds only one object of each value, and Map is an associative array that lets you associate objects with other objects—the Java container classes will automatically resize themselves. So, unlike with arrays, you can put in any number of objects and you don’t need to worry about how big to make the container while you’re writing the program. Even though they don’t have direct keyword support in Java,1container classes are fundamental tools that significantly increase your programming muscle. In this chapter you’ll get a basic working knowledge of the Java container library, with an emphasis on typical usage. Here, we’ll focus on the containers that you’ll use in day-to-day programming. Later, in the Containers in Depth chapter, you’ll learn about the rest of the containers and more details about their functionality and how to use them. 1A number of languages, such as Perl, Python, and Ruby, have native support for containers. Generics and type-safe containers One of the problems of using pre-Java SE5 containers was that the compiler allowed you to insert an incorrect type into a container. For example, consider a container of Apple objects, using the basic workhorse container, ArrayList. For now, you can think of ArrayList as "an array that automatically expands itself." Using an ArrayList is straightforward: Create one, insert objects using add( ), and access them with get( ), using an index—just as you do with an array, but without the square brackets.2ArrayList also has a method size( ) to let you know how many elements have been added, so that you don’t inadvertently index off the end and cause an error (by throwing a runtime exception; exceptions will be introduced in the chapter Error Handling with Exceptions). In this example, Apples and Oranges are placed into the container, then pulled out. Normally, the Java compiler will give you a warning because the example does not use generics. Here, a special Java SE5 annotation is used to suppress the warning. Annotations start with an ‘@’ sign, and can take an argument; this one is @SuppressWarnings and the argument indicates that "unchecked" warnings only should be suppressed:
```java
//: holding/ApplesAndOrangesWithoutGenerics.java
// Simple container example (produces compiler warnings).
// {ThrowsException}
import java.util.*;
class Apple {
private static long counter;
private final long id = counter++;
public long id() { return id; }
}
class Orange {}
public class ApplesAndOrangesWithoutGenerics {
@SuppressWarnings("unchecked")
public static void main(String[] args) {
ArrayList apples = new ArrayList();
for(int i = 0; i < 3; i++)
apples.add(new Apple());
// Not prevented from adding an Orange to apples:
apples.add(new Orange());
for(int i = 0; i < apples.size(); i++)
((Apple)apples.get(i)).id();
// Orange is detected only at run time
}
} /* (Execute to see output) *///:~
```

<!--p299-->
You’ll learn more about Java SE5 annotations in the Annotations chapter. The classes Apple and Orange are distinct; they have nothing in common except that they are both Objects. (Remember that if you don’t explicitly say what class you’re inheriting from, you automatically inherit from Object.)Since ArrayList holds Objects, you can not only add Apple objects into this container using the ArrayList method add( ), but you can also add Orange objects without complaint at either compile time or run time. When you go to fetch out what you think are Apple objects using the ArrayList method get( ), you get back a reference to an Object that you must cast to an Apple. Then you need to surround the entire expression with parentheses to force the evaluation of the cast before calling the 2This is a place where operator overloading would have been nice. C++ and C# container classes produce a cleaner syntax using operator overloading. Holding Your Objects id( ) method for Apple;otherwise, you’ll get a syntax error. At run time, when you try to cast the Orange object to an Apple, you’ll get an error in the form of the aforementioned exception. In the Generics chapter, you’ll learn that creating classes using Java generics can be complex. However, applying predefined generic classes is usually straightforward. For example, to define an ArrayList intended to hold Apple objects, you say ArrayList<Apple> instead of just ArrayList. The angle brackets surround the type parameters (there may be more than one), which specify the type(s) that can be held by that instance of the container. With generics, you’re prevented, at compile time, from putting the wrong type of object into a container.3 Here’s the example again, using generics:
```java
//: holding/ApplesAndOrangesWithGenerics.java
import java.util.*;
public class ApplesAndOrangesWithGenerics {
public static void main(String[] args) {
ArrayList<Apple> apples = new ArrayList<Apple>();
for(int i = 0; i < 3; i++)
apples.add(new Apple());
// Compile-time error:
// apples.add(new Orange());
for(int i = 0; i < apples.size(); i++)
System.out.println(apples.get(i).id());
// Using foreach:
for(Apple c : apples)
System.out.println(c.id());
}
} /* Output:
*///:~
```
Now the compiler will prevent you from putting an Orange into apples, so it becomes a compile-time error rather than a runtime error. Also notice that the cast is no longer necessary when fetching items back out from the List. Since the List knows what type it holds, it does the cast for you when you call get( ). Thus, with generics you not only know that the compiler will check the type of object that you put into a container, but you also get cleaner syntax when using the objects in the container. The example also shows that, if you do not need to use the index of each element, you can use the foreach syntax to select each element in the List. You are not limited to putting the exact type of object into a container when you specify that type as a generic parameter. Upcasting works the same with generics as it does with other types:
```java
//: holding/GenericsAndUpcasting.java
import java.util.*;
class GrannySmith extends Apple {}
class Gala extends Apple {}
class Fuji extends Apple {}
class Braeburn extends Apple {}
public class GenericsAndUpcasting {
public static void main(String[] args) {
ArrayList<Apple> apples = new ArrayList<Apple>();
apples.add(new GrannySmith());
```

<!--p300-->
3At the end of the Generics chapter, you’ll find a discussion about whether this is such a bad problem. However, the Generics chapter will also show you that Java generics are useful for more than just type-safe containers.
```java
apples.add(new Gala());
apples.add(new Fuji());
apples.add(new Braeburn());
for(Apple c : apples)
System.out.println(c);
}
} /* Output: (Sample)
GrannySmith@7d772e
Gala@11b86e7
Fuji@35ce36
Braeburn@757aef
*///:~
```
Thus, you can add a subtype of Apple to a container that is specified to hold Apple objects. The output is produced from the default toString( ) method of Object, which prints the class name followed by the unsigned hexadecimal representation of the hash code of the object (generated by the hashCode( ) method). You’ll learn about hash codes in detail in Containers in Depth. Exercise 1:(2) Create a new class called Gerbil with an int gerbilNumber that’s initialized in the constructor. Give it a method called hop( ) that displays which gerbil number this is, and that it’s hopping. Create an ArrayList and add Gerbil objects to the List. Now use the get( ) method to move through the List and call hop( ) for each Gerbil. Basic concepts The Java container library takes the idea of "holding your objects" and divides it into two distinct concepts, expressed as the basic interfaces of the library: 1.Collection:a sequence of individual elements with one or more rules applied to them. A List must hold the elements in the way that they were inserted, a Set cannot have duplicate elements, and a Queue produces the elements in the order determined by a queuing discipline (usually the same order in which they are inserted). 2.Map: a group of key-value object pairs, allowing you to look up a value using a key. An ArrayList allows you to look up an object using a number, so in a sense it associates numbers to objects. A map allows you to look up an object using another object. It’s also called an associative array, because it associates objects with other objects, or a dictionary, because you look up a value object using a key object just like you look up a definition using a word. Maps are powerful programming tools. Although it’s not always possible, ideally you’ll write most of your code to talk to these interfaces, and the only place where you’ll specify the precise type you’re using is at the point of creation. So you can create a List like this:
```java
List<Apple> apples = new ArrayList<Apple>();
```
Notice that the ArrayList has been upcast to a List, in contrast to the way it was handled in the previous examples. The intent of using the interface is that if you decide you want to change your implementation, all you need to do is change it at the point of creation, like this:
```java
List<Apple> apples = new LinkedList<Apple>();
```

<!--p301-->
Thus, you’ll typically make an object of a concrete class, upcast it to the corresponding interface, and then use the interface throughout the rest of your code. This approach won’t always work, because some classes have additional functionality. For example, LinkedList has additional methods that are not in the List interface, and a TreeMap has methods that are not in the Map interface. If you need to use those methods, you won’t be able to upcast to the more general interface. The Collection interface generalizes the idea of a sequence—a way of holding a group of objects. Here’s a simple example that fills a Collection (represented here with an ArrayList) with Integer objects and then prints each element in the resulting container:
```java
//: holding/SimpleCollection.java
import java.util.*;
public class SimpleCollection {
public static void main(String[] args) {
Collection<Integer> c = new ArrayList<Integer>();
for(int i = 0; i < 10; i++)
c.add(i); // Autoboxing
for(Integer i : c)
System.out.print(i + ", ");
}
} /* Output:
0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
*///:~
```
Since this example only uses Collection methods, any object of a class inherited from Collection would work, but ArrayList is the most basic type of sequence. The name of the add( ) method suggests that it puts a new element in the Collection. However, the documentation carefully states that add( ) "ensures that this Collection contains the specified element." This is to allow for the meaning of Set, which adds the element only if it isn’t already there. With an ArrayList, or any sort of List, add( ) always means "put it in," because Lists don’t care if there are duplicates. All Collections can be traversed using the foreach syntax, as shown here. Later in this chapter you’ll learn about a more flexible concept called an Iterator. Exercise 2:(1) Modify SimpleCollection.java to use a Set for c. Exercise 3:(2) Modify innerclasses/Sequence.java so that you can add any number of elements to it. Adding groups of elements There are utility methods in both the Arrays and Collections classes in java.util that add groups of elements to a Collection. Arrays.asList( ) takes either an array or a comma- separated list of elements (using varargs) and turns it into a List object. Collections.addAll( ) takes a Collection object and either an array or a comma-separated list and adds the elements to the Collection. Here’s an example that shows both methods, as well as the more conventional addAll( ) method that’s part of all Collection types:
```java
//: holding/AddingGroups.java
// Adding groups of elements to Collection objects.
import java.util.*;
public class AddingGroups {
public static void main(String[] args) {
Collection<Integer> collection =
```

<!--p302-->
Holding Your Objects
```java
new ArrayList<Integer>(Arrays.asList(1, 2, 3, 4, 5));
Integer[] moreInts = { 6, 7, 8, 9, 10 };
collection.addAll(Arrays.asList(moreInts));
// Runs significantly faster, but you can’t
// construct a Collection this way:
Collections.addAll(collection, 11, 12, 13, 14, 15);
Collections.addAll(collection, moreInts);
// Produces a list "backed by" an array:
List<Integer> list = Arrays.asList(16, 17, 18, 19, 20);
list.set(1, 99); // OK -- modify an element
// list.add(21); // Runtime error because the
// underlying array cannot be resized.
}
} ///:~
```
The constructor for a Collection can accept another Collection which it uses for initializing itself, so you can use Arrays.asList( ) to produce input for the constructor. However, Collections.addAll( ) runs much faster, and it’s just as easy to construct the Collection with no elements and then call Collections.addAll( ), so this is the preferred approach. The Collection.addAll( ) member method can only take an argument of another Collection object, so it is not as flexible as Arrays.asList( ) or Collections.addAll( ), which use variable argument lists. It’s also possible to use the output of Arrays.asList( ) directly, as a List, but the underlying representation in this case is the array, which cannot be resized. If you try to add( ) or delete( ) elements in such a list, that would attempt to change the size of an array, so you’ll get an "Unsupported Operation" error at run time. A limitation of Arrays.asList( ) is that it takes a best guess about the resulting type of the List, and doesn’t pay attention to what you’re assigning it to. Sometimes this can cause a problem:

<!--p303-->
```java
//: holding/AsListInference.java
// Arrays.asList() makes its best guess about type.
import java.util.*;
class Snow {}
class Powder extends Snow {}
class Light extends Powder {}
class Heavy extends Powder {}
class Crusty extends Snow {}
class Slush extends Snow {}
public class AsListInference {
public static void main(String[] args) {
List<Snow> snow1 = Arrays.asList(
new Crusty(), new Slush(), new Powder());
// Won’t compile:
// List<Snow> snow2 = Arrays.asList(
// new Light(), new Heavy());
// Compiler says:
// found : java.util.List<Powder>
// required: java.util.List<Snow>
// Collections.addAll() doesn’t get confused:
List<Snow> snow3 = new ArrayList<Snow>();
Collections.addAll(snow3, new Light(), new Heavy());
// Give a hint using an
// explicit type argument specification:
List<Snow> snow4 = Arrays.<Snow>asList(
new Light(), new Heavy());
}
} ///:~
```
When trying to create snow2, Arrays.asList( ) only has types of Powder, so it creates a List<Powder> rather than a List<Snow>, whereas Collections.addAll( ) works fine because it knows from the first argument what the target type is. As you can see from the creation of snow4, it’s possible to insert a "hint" in the middle of Arrays.asList( ), to tell the compiler what the actual target type should be for the resulting List type produced by Arrays.asList( ). This is called an explicit type argument specification. Maps are more complex, as you’ll see, and the Java standard library does not provide any way to automatically initialize them, except from the contents of another Map. Printing containers You must use Arrays.toString( ) to produce a printable representation of an array, but the containers print nicely without any help. Here’s an example that also introduces you to the basic Java containers:
```java
//: holding/PrintingContainers.java
// Containers print themselves automatically.
import java.util.*;
import static net.mindview.util.Print.*;
public class PrintingContainers {
static Collection fill(Collection<String> collection) {
collection.add("rat");
collection.add("cat");
collection.add("dog");
collection.add("dog");
return collection;
}
static Map fill(Map<String,String> map) {
map.put("rat", "Fuzzy");
map.put("cat", "Rags");
map.put("dog", "Bosco");
map.put("dog", "Spot");
return map;
}
public static void main(String[] args) {
print(fill(new ArrayList<String>()));
print(fill(new LinkedList<String>()));
print(fill(new HashSet<String>()));
print(fill(new TreeSet<String>()));
print(fill(new LinkedHashSet<String>()));
print(fill(new HashMap<String,String>()));
print(fill(new TreeMap<String,String>()));
print(fill(new LinkedHashMap<String,String>()));
}
} /* Output:
[rat, cat, dog, dog]
[rat, cat, dog, dog]
[dog, cat, rat]
```

<!--p304-->
Holding Your Objects
```java
[cat, dog, rat]
[rat, cat, dog]
{dog=Spot, cat=Rags, rat=Fuzzy}
{cat=Rags, dog=Spot, rat=Fuzzy}
{rat=Fuzzy, cat=Rags, dog=Spot}
*///:~
```

<!--p305-->
This shows the two primary categories in the Java container library. The distinction is based on the number of items that are held in each "slot" in the container. The Collection category only holds one item in each slot. It includes the List, which holds a group of items in a specified sequence, the Set, which only allows the addition of one identical item, and the Queue, which only allows you to insert objects at one "end" of the container and remove objects from the other "end" (for the purposes of this example, this is just another way of looking at a sequence and so it is not shown). A Map holds two objects, a key and an associated value, in each slot. In the output, you can see that the default printing behavior (provided via each container’s toString( ) method) produces reasonably readable results. A Collection is printed surrounded by square brackets, with each element separated by a comma. A Map is surrounded by curly braces, with each key and value associated with an equal sign (keys on the left, values on the right). The first fill( ) method works with all types of Collection, each of which implements the add( ) method to include new elements. ArrayList and LinkedList are both types of List, and you can see from the output that they both hold elements in the same order in which they are inserted. The difference between the two is not only performance for certain types of operations, but also that a LinkedList contains more operations than an ArrayList. These will be explored more fully later in this chapter. HashSet, TreeSet and LinkedHashSet are types of Set. The output shows that a Set will only hold one of each identical item, but it also shows that the different Set implementations store the elements differently. The HashSet stores elements using a rather complex approach that will be explored in the Containers in Depth chapter—all you need to know at this point is that this technique is the fastest way to retrieve elements, and as a result the storage order can seem nonsensical (often, you only care whether something is a member of the Set, not the order in which it appears). If storage order is important, you can use a TreeSet, which keeps the objects in ascending comparison order, or a LinkedHashSet, which keeps the objects in the order in which they were added. A Map (also called an associative array) allows you to look up an object using a key, like a simple database. The associated object is called a value. If you have a Map that associates states with their capitals and you want to know the capital of Ohio, you look it up using "Ohio" as the key—almost as if you were indexing into an array. Because of this behavior, a Map only accepts one of each key. Map.put(key, value) adds a value (the thing you want) and associates it with a key (the thing you look it up with). Map.get(key) produces the value associated with that key. The above example only adds key-value pairs, and does not perform lookups. That will be shown later. Notice that you don’t have to specify (or think about) the size of the Map because it resizes itself automatically. Also, Maps know how to print themselves, showing the association with keys and values. The order that the keys and values are held inside the Map is not the insertion order because the HashMap implementation uses a very fast algorithm that controls the order. The example uses the three basic flavors of Map: HashMap, TreeMap and LinkedHashMap. Like HashSet, HashMap provides the fastest lookup technique, and also doesn’t hold its elements in any apparent order. A TreeMap keeps the keys sorted by ascending comparison order, and a LinkedHashMap keeps the keys in insertion order while retaining the lookup speed of the HashMap. Exercise 4:(3) Create a generator class that produces character names (as String objects) from your favorite movie (you can use Snow White or Star Wars as a fallback) each time you call next( ), and loops around to the beginning of the character list when it runs out of names. Use this generator to fill an array, an ArrayList, a LinkedList, a HashSet, a LinkedHashSet, and a TreeSet, then print each container.
## List
Lists promise to maintain elements in a particular sequence. The List interface adds a number of methods to Collection that allow insertion and removal of elements in the middle of a List. There are two types of List: • The basic ArrayList, which excels at randomly accessing elements, but is slower when inserting and removing elements in the middle of a List. • The LinkedList, which provides optimal sequential access, with inexpensive insertions and deletions from the middle of the List. A LinkedList is relatively slow for random access, but it has a larger feature set than the ArrayList. The following example reaches forward in the book to use a library from the Type Information chapter by importing typeinfo.pets. This is a library that contains a hierarchy of Pet classes along with some tools to randomly generate Pet objects. You don’t need to know the full details at this point, just that (1) there’s a Pet class and various subtypes of Pet and (2) the static Pets.arrayList( ) method will return an ArrayList filled with randomly selected Pet objects:
```java
//: holding/ListFeatures.java
import typeinfo.pets.*;
import java.util.*;
import static net.mindview.util.Print.*;
public class ListFeatures {
public static void main(String[] args) {
Random rand = new Random(47);
List<Pet> pets = Pets.arrayList(7);
print("1: " + pets);
Hamster h = new Hamster();
pets.add(h); // Automatically resizes
print("2: " + pets);
print("3: " + pets.contains(h));
pets.remove(h); // Remove by object
Pet p = pets.get(2);
print("4: " + p + " " + pets.indexOf(p));
Pet cymric = new Cymric();
print("5: " + pets.indexOf(cymric));
print("6: " + pets.remove(cymric));
// Must be the exact object:
print("7: " + pets.remove(p));
print("8: " + pets);
pets.add(3, new Mouse()); // Insert at an index
```

<!--p306-->
Holding Your Objects

<!--p307-->
```java
print("9: " + pets);
List<Pet> sub = pets.subList(1, 4);
print("subList: " + sub);
print("10: " + pets.containsAll(sub));
Collections.sort(sub); // In-place sort
print("sorted subList: " + sub);
// Order is not important in containsAll():
print("11: " + pets.containsAll(sub));
Collections.shuffle(sub, rand); // Mix it up
print("shuffled subList: " + sub);
print("12: " + pets.containsAll(sub));
List<Pet> copy = new ArrayList<Pet>(pets);
sub = Arrays.asList(pets.get(1), pets.get(4));
print("sub: " + sub);
copy.retainAll(sub);
print("13: " + copy);
copy = new ArrayList<Pet>(pets); // Get a fresh copy
copy.remove(2); // Remove by index
print("14: " + copy);
copy.removeAll(sub); // Only removes exact objects
print("15: " + copy);
copy.set(1, new Mouse()); // Replace an element
print("16: " + copy);
copy.addAll(2, sub); // Insert a list in the middle
print("17: " + copy);
print("18: " + pets.isEmpty());
pets.clear(); // Remove all elements
print("19: " + pets);
print("20: " + pets.isEmpty());
pets.addAll(Pets.arrayList(4));
print("21: " + pets);
Object[] o = pets.toArray();
print("22: " + o[3]);
Pet[] pa = pets.toArray(new Pet[0]);
print("23: " + pa[3].id());
}
} /* Output:
1: [Rat, Manx, Cymric, Mutt, Pug, Cymric, Pug]
2: [Rat, Manx, Cymric, Mutt, Pug, Cymric, Pug, Hamster]
3: true
4: Cymric 2
5: -1
6: false
7: true
8: [Rat, Manx, Mutt, Pug, Cymric, Pug]
9: [Rat, Manx, Mutt, Mouse, Pug, Cymric, Pug]
subList: [Manx, Mutt, Mouse]
10: true
sorted subList: [Manx, Mouse, Mutt]
11: true
shuffled subList: [Mouse, Manx, Mutt]
12: true
sub: [Mouse, Pug]
13: [Mouse, Pug]
14: [Rat, Mouse, Mutt, Pug, Cymric, Pug]
15: [Rat, Mutt, Cymric, Pug]
16: [Rat, Mouse, Cymric, Pug]
17: [Rat, Mouse, Mouse, Pug, Cymric, Pug]
18: false
19: []
20: true
21: [Manx, Cymric, Rat, EgyptianMau]
22: EgyptianMau
23: 14
*///:~
```

<!--p308-->
The print lines are numbered so the output can be related to the source code. The first output line shows the original List of Pets. Unlike an array, a List allows you to add elements after it has been created, or remove elements, and it resizes itself. That’s its fundamental value: a modifiable sequence. You can see the result of adding a Hamster in output line 2—the object is appended to the end of the list. You can find out whether an object is in the list using the contains( ) method. If you want to remove an object, you can pass that object’s reference to the remove( ) method. Also, if you have a reference to an object, you can discover the index number where that object is located in the List using indexOf( ), as you can see in output line 4. When deciding whether an element is part of a List, discovering the index of an element, and removing an element from a List by reference, the equals( ) method (part of the root class Object) is used. Each Pet is defined to be a unique object, so even though there are two Cymricsin the list, if I create a new Cymric object and pass it to indexOf( ), the result will be -1 (indicating it wasn’t found), and attempts to remove( ) the object will return false. For other classes, equals( ) may be defined differently—Strings, for example, are equal if the contents of two Strings are identical. So to prevent surprises, it’s important to be aware that List behavior changes depending on equals( ) behavior. In output lines 7 and 8, removing an object that exactly matches an object in the List is shown to be successful. It’s possible to insert an element in the middle of the List, as you can see in output line 9 and the code that precedes it, but this brings up an issue: for a LinkedList, insertion and removal in the middle of a list is a cheap operation (except for, in this case, the actual random access into the middle of the list), but for an ArrayList it is an expensive operation. Does this mean you should never insert elements in the middle of an ArrayList, and switch to a LinkedList if you do? No, it just means you should be aware of the issue, and if you start doing many insertions in the middle of an ArrayList and your program starts slowing down, that you might look at your List implementation as the possible culprit (the best way to discover such a bottleneck, as you will see in the supplement at http://MindView.net/Books/BetterJava, is to use a profiler). Optimization is a tricky issue, and the best policy is to leave it alone until you discover you need to worry about it (although understanding the issues is always a good idea). The subList( ) method allows you to easily create a slice out of a larger list, and this naturally produces a true result when passed to containsAll( ) for that larger list. It’s also interesting to note that order is unimportant—you can see in output lines 11 and 12 that calling the intuitively named Collections.sort( ) and Collections.shuffle( ) on sub doesn’t affect the outcome of containsAll( ). subList( ) produces a list backed by the original list. Therefore, changes in the returned list are reflected in the original list, and vice versa. The retainAll( ) method is effectively a "set intersection" operation, in this case keeping all the elements in copy that are also in sub. Again, the resulting behavior depends on the equals( ) method. Output line 14 shows the result of removing an element using its index number, which is more straightforward than removing it by object reference since you don’t have to worry about equals( ) behavior when using indexes. The removeAll( ) method also operates based on the equals( ) method. As the name implies, it removes all the objects from the List that are in the argument List. The set( ) method is rather unfortunately named because of the potential confusion with the Set class— Holding Your Objects "replace" might have been a better name here, because it replaces the element at the index (the first argument) with the second argument. Output line 17 shows that for Lists, there’s an overloaded addAll( ) method that allows you to insert the new list in the middle of the original list, instead of just appending it to the end with the addAll( ) that comes from Collection. Output lines 18-20 show the effect of the isEmpty( ) and clear( ) methods. Output lines 22 and 23 show how you can convert any Collection to an array using toArray( ). This is an overloaded method; the no-argument version returns an array of Object, but if you pass an array of the target type to the overloaded version, it will produce an array of the type specified (assuming it passes type checking). If the argument array is too small to hold all the objects in the List (as is the case here), to Array( ) will create a new array of the appropriate size. Pet objects have an id( ) method, which you can see is called on one of the objects in the resulting array. Exercise 5:(3) Modify ListFeatures.java so that it uses Integers (remember autoboxing!) instead of Pets, and explain any difference in results. Exercise 6:(2) Modify ListFeatures.java so that it uses Strings instead of Pets, and explain any difference in results. Exercise 7:(3) Create a class, then make an initialized array of objects of your class. Fill a List from your array. Create a subset of your List by using subList( ), then remove this subset from your List.
## Iterator

<!--p309-->
In any container, you must have a way to insert elements and fetch them out again. After all, that’s the primary job of a container—to hold things. In a List, add( ) is one way to insert elements, and get( ) is one way to fetch elements. If you want to start thinking at a higher level, there’s a drawback: You need to program to the exact type of the container in order to use it. This might not seem bad at first, but what if you write code for a List, and later on you discover that it would be convenient to apply that same code to a Set?Or suppose you’d like to write, from the beginning, a piece of general- purpose code that doesn’t know or care what type of container it’s working with, so that it can be used on different types of containers without rewriting that code? The concept of an Iterator (another design pattern) can be used to achieve this abstraction. An iterator is an object whose job is to move through a sequence and select each object in that sequence without the client programmer knowing or caring about the underlying structure of that sequence. In addition, an iterator is usually what’s called a lightweight object: one that’s cheap to create. For that reason, you’ll often find seemingly strange constraints for iterators; for example, the Java Iterator can move in only one direction. There’s not much you can do with an Iterator except: 1.Ask a Collection to hand you an Iterator using a method called iterator( ). That Iterator will be ready to return the first element in the sequence. 2.Get the next object in the sequence with next( ). 3. See if there are any more objects in the sequence with hasNext( ). Holding Your Objects 4. Remove the last element returned by the iterator with remove( ). To see how it works, we can again use the Pets tools from the Type Information chapter:
```java
//: holding/SimpleIteration.java
import typeinfo.pets.*;
import java.util.*;
public class SimpleIteration {
public static void main(String[] args) {
List<Pet> pets = Pets.arrayList(12);
Iterator<Pet> it = pets.iterator();
while(it.hasNext()) {
Pet p = it.next();
System.out.print(p.id() + ":" + p + " ");
}
System.out.println();
// A simpler approach, when possible:
for(Pet p : pets)
System.out.print(p.id() + ":" + p + " ");
System.out.println();
// An Iterator can also remove elements:
it = pets.iterator();
for(int i = 0; i < 6; i++) {
it.next();
it.remove();
}
System.out.println(pets);
}
} /* Output:
0:Rat 1:Manx 2:Cymric 3:Mutt 4:Pug 5:Cymric 6:Pug 7:Manx 8:Cymric 9:Rat
10:EgyptianMau 11:Hamster
0:Rat 1:Manx 2:Cymric 3:Mutt 4:Pug 5:Cymric 6:Pug 7:Manx 8:Cymric 9:Rat
10:EgyptianMau 11:Hamster
[Pug, Manx, Cymric, Rat, EgyptianMau, Hamster]
*///:~
```
With an Iterator, you don’t need to worry about the number of elements in the container. That’s taken care of for you by hasNext( ) and next( ). If you’re simply moving forward through the List and not trying to modify the List object itself, you can see that the foreach syntax is more succinct. An Iterator will also remove the last element produced by next( ), which means you must call next( ) before you call remove( ).4 This idea of taking a container of objects and passing through it to perform an operation on each one is powerful and will be seen throughout this book. Now consider the creation of a display( ) method that is container-agnostic:
```java
//: holding/CrossContainerIteration.java
import typeinfo.pets.*;
import java.util.*;
public class CrossContainerIteration {
```

<!--p310-->
4remove( ) is a so-called "optional" method (there are other such methods), which means that not all Iterator implementations must implement it. This topic is covered in the Containers in Depth chapter. The standard Java library containers implement remove( ), however, so you don’t need to worry about it until that chapter.
```java
public static void display(Iterator<Pet> it) {
while(it.hasNext()) {
Pet p = it.next();
System.out.print(p.id() + ":" + p + " ");
}
System.out.println();
}
public static void main(String[] args) {
ArrayList<Pet> pets = Pets.arrayList(8);
LinkedList<Pet> petsLL = new LinkedList<Pet>(pets);
HashSet<Pet> petsHS = new HashSet<Pet>(pets);
TreeSet<Pet> petsTS = new TreeSet<Pet>(pets);
display(pets.iterator());
display(petsLL.iterator());
display(petsHS.iterator());
display(petsTS.iterator());
}
} /* Output:
0:Rat 1:Manx 2:Cymric 3:Mutt 4:Pug 5:Cymric 6:Pug 7:Manx
0:Rat 1:Manx 2:Cymric 3:Mutt 4:Pug 5:Cymric 6:Pug 7:Manx
4:Pug 6:Pug 3:Mutt 1:Manx 5:Cymric 7:Manx 2:Cymric 0:Rat
5:Cymric 2:Cymric 7:Manx 1:Manx 3:Mutt 6:Pug 4:Pug 0:Rat
*///:~
```
Note that display( ) contains no information about the type of sequence that it is traversing, and this shows the true power of the Iterator:the ability to separate the operation of traversing a sequence from the underlying structure of that sequence. For this reason, we sometimes say that iterators unify access to containers. Exercise 8:(1) Modify Exercise l so it uses an Iterator to move through the List while calling hop( ). Exercise 9:(4) Modify innerclasses/Sequence.java so that Sequence works with an Iterator instead of a Selector. Exercise 10:(2) Change Exercise 9 in the Polymorphism chapter to use an ArrayList to hold the Rodents and an Iterator to move through the sequence of Rodents. Exercise 11:(2) Write a method that uses an Iterator to step through a Collection and print the toString( ) of each object in the container. Fill all the different types of Collections with objects and apply your method to each container.
## ListIterator
The ListIterator is a more powerful subtype of Iterator that is produced only by List classes. While Iterator can only move forward, ListIterator is bidirectional. It can also produce the indexes of the next and previous elements relative to where the iterator is pointing in the list, and it can replace the last element that it visited using the set( ) method. You can produce a ListIterator that points to the beginning of the List by calling listIterator( ), and you can also create a ListIterator that starts out pointing to an index n in the list by calling listIterator(n). Here’s an example that demonstrates all these abilities:

<!--p311-->
```java
//: holding/ListIteration.java
import typeinfo.pets.*;
import java.util.*;
public class ListIteration {
public static void main(String[] args) {
List<Pet> pets = Pets.arrayList(8);
ListIterator<Pet> it = pets.listIterator();
while(it.hasNext())
System.out.print(it.next() + ", " + it.nextIndex() +
", " + it.previousIndex() + "; ");
System.out.println();
// Backwards:
while(it.hasPrevious())
System.out.print(it.previous().id() + " ");
System.out.println();
System.out.println(pets);
it = pets.listIterator(3);
while(it.hasNext()) {
it.next();
it.set(Pets.randomPet());
}
System.out.println(pets);
}
} /* Output:
Rat, 1, 0; Manx, 2, 1; Cymric, 3, 2; Mutt, 4, 3; Pug, 5, 4; Cymric, 6,
5; Pug, 7, 6; Manx, 8, 7;
7 6 5 4 3 2 1 0
[Rat, Manx, Cymric, Mutt, Pug, Cymric, Pug, Manx]
[Rat, Manx, Cymric, Cymric, Rat, EgyptianMau, Hamster, EgyptianMau]
*///:~
```
The Pets.randomPet( ) method is used to replace all the Pet objects in the List from location 3 onward. Exercise 12:(3) Create and populate a List<Integer>. Create a second List<Integer> of the same size as the first, and use ListIteratorsto read elements from the first List and insert them into the second in reverse order. (You may want to explore a number of different ways to solve this problem.)
## LinkedList

<!--p312-->
The LinkedList also implements the basic List interface like ArrayList does, but it performs certain operations (insertion and removal in the middle of the List) more efficiently than does ArrayList. Conversely, it is less efficient for random-access operations. LinkedList also adds methods that allow it to be used as a stack, a Queue or a double- ended queue (deque). Some of these methods are aliases or slight variations of each other, to produce names that are more familiar within the context of a particular usage (Queue, in particular). For example, getFirst( ) and element( ) are identical—they return the head (first element) of the list without removing it, and throw NoSuchElementException if the List is empty. peek( ) is a slight variation of those two that returns null if the list is empty. removeFirst( ) and remove( ) are also identical—they remove and return the head of the list, and throw NoSuchElementException for an empty list, and poll( ) is a slight variation that returns null if this list is empty. addFirst( ) inserts an element at the beginning of the list. offer( ) is the same as add( ) and addLast( ). They all add an element to the tail (end) of a list. Holding Your Objects removeLast( ) removes and returns the last element of the list. Here’s an example that shows the basic similarity and differences between these features. It doesn’t repeat the behavior that was shown in ListFeatures.java:
```java
//: holding/LinkedListFeatures.java
import typeinfo.pets.*;
import java.util.*;
import static net.mindview.util.Print.*;
public class LinkedListFeatures {
public static void main(String[] args) {
LinkedList<Pet> pets =
new LinkedList<Pet>(Pets.arrayList(5));
print(pets);
// Identical:
print("pets.getFirst(): " + pets.getFirst());
print("pets.element(): " + pets.element());
// Only differs in empty-list behavior:
print("pets.peek(): " + pets.peek());
// Identical; remove and return the first element:
print("pets.remove(): " + pets.remove());
print("pets.removeFirst(): " + pets.removeFirst());
// Only differs in empty-list behavior:
print("pets.poll(): " + pets.poll());
print(pets);
pets.addFirst(new Rat());
print("After addFirst(): " + pets);
pets.offer(Pets.randomPet());
print("After offer(): " + pets);
pets.add(Pets.randomPet());
print("After add(): " + pets);
pets.addLast(new Hamster());
print("After addLast(): " + pets);
print("pets.removeLast(): " + pets.removeLast());
}
} /* Output:
[Rat, Manx, Cymric, Mutt, Pug]
pets.getFirst(): Rat
pets.element(): Rat
pets.peek(): Rat
pets.remove(): Rat
pets.removeFirst(): Manx
pets.poll(): Cymric
[Mutt, Pug]
After addFirst(): [Rat, Mutt, Pug]
After offer(): [Rat, Mutt, Pug, Cymric]
After add(): [Rat, Mutt, Pug, Cymric, Pug]
After addLast(): [Rat, Mutt, Pug, Cymric, Pug, Hamster]
pets.removeLast(): Hamster
*///:~
```

<!--p313-->
The result of Pets.arrayList( ) is handed to the LinkedList constructor in order to populate it. If you look at the Queue interface, you’ll see the element( ), offer( ), peek( ), poll( ) and remove( ) methods that were added to LinkedList in order that it could be a Queue implementation. Full examples of Queues will be given later in this chapter. Exercise 13: (3)Inthe innerclasses/GreenhouseController.java example, the class Controller uses an ArrayList. Change the code to use a LinkedList instead, and use an Iterator to cycle through the set of events. Exercise 14: (3) Create an empty LinkedList<Integer>. Using a Listlterator, add Integers to the List by always inserting them in the middle of the List.
## Stack
A stack is sometimes referred to as a "last-in, first-out" (LIFO) container. It’s sometimes called a pushdown stack, because whatever you "push" on the stack last is the first item you can "pop" off of the stack. An often-used analogy is of cafeteria trays in a spring-loaded holder—the last ones that go in are the first ones that come out. LinkedList has methods that directly implement stack functionality, so you can also just use a LinkedList rather than making a stack class. However, a stack class can sometimes tell the story better:
```java
//: net/mindview/util/Stack.java
// Making a stack from a LinkedList.
package net.mindview.util;
import java.util.LinkedList;
public class Stack<T> {
private LinkedList<T> storage = new LinkedList<T>();
public void push(T v) { storage.addFirst(v); }
public T peek() { return storage.getFirst(); }
public T pop() { return storage.removeFirst(); }
public boolean empty() { return storage.isEmpty(); }
public String toString() { return storage.toString(); }
} ///:~
```
This introduces the simplest possible example of a class definition using generics. The <T> after the class name tells the compiler that this will be a parameterized type, and that the type parameter—the one that will be substituted with a real type when the class is used—is T. Basically, this says, "We’re defining a Stack that holds objects of type T."The Stack is implemented using a LinkedList, and the LinkedList is also told that it is holding type T. Notice that push( ) takes an object of type T, while peek( ) and pop( ) return an object of type T. The peek( ) method provides you with the top element without removing it from the top of the stack, while pop( ) removes and returns the top element. If you want only stack behavior, inheritance is inappropriate here because it would produce a class with all the rest of the LinkedList methods (you’ll see in the Containers in Depth chapter that this very mistake was made by the Java l.o designers when they created java.util.Stack). Here’s a simple demonstration of this new Stack class:
```java
//: holding/StackTest.java
import net.mindview.util.*;
public class StackTest {
public static void main(String[] args) {
Stack<String> stack = new Stack<String>();
for(String s : "My dog has fleas".split(" "))
stack.push(s);
while(!stack.empty())
System.out.print(stack.pop() + " ");
}
} /* Output:
fleas has dog My
*///:~
```

<!--p314-->
Holding Your Objects If you want to use this Stack class in your own code, you’ll need to fully specify the package— or change the name of the class—when you create one; otherwise, you’ll probably collide with the Stack in the java.util package. For example, if we import java.util.* into the above example, we must use package names in order to prevent collisions:
```java
//: holding/StackCollision.java
import net.mindview.util.*;
public class StackCollision {
public static void main(String[] args) {
net.mindview.util.Stack<String> stack =
new net.mindview.util.Stack<String>();
for(String s : "My dog has fleas".split(" "))
stack.push(s);
while(!stack.empty())
System.out.print(stack.pop() + " ");
System.out.println();
java.util.Stack<String> stack2 =
new java.util.Stack<String>();
for(String s : "My dog has fleas".split(" "))
stack2.push(s);
while(!stack2.empty())
System.out.print(stack2.pop() + " ");
}
} /* Output:
fleas has dog My
fleas has dog My
*///:~
```
The two Stack classes have the same interface, but there is no common Stack interface in java.util—probably because the original, poorly designed java.util.Stack class in Java 1.0 co-opted the name. Even though java.util.Stack exists, LinkedList produces a better Stack and so the net.mindview.util.Stack approach is preferable. You can also control the selection of the "preferred" Stack implementation using an explicit import:
```java
import net.mindview.util.Stack;
```
Now any reference to Stack will select the net.mindview.util version, and to select java.util.Stack you must use full qualification. Exercise 15:(4) Stacks are often used to evaluate expressions in programming languages. Using net.mindview.util.Stack, evaluate the following expression, where’+’ means "push the following letter onto the stack," and’-’ means "pop the top of the stack and print it": "+U+n+c—+e+r+t—+a-+i-+n+t+y—+ -+r+u—+l+e+s—"
## Set

<!--p315-->
A Set refuses to hold more than one instance of each object value. If you try to add more than one instance of an equivalent object, the Set prevents duplication. The most common use for a Set is to test for membership, so that you can easily ask whether an object is in a Set. Because of this, lookup is typically the most important operation for a Set, so you’ll usually choose a HashSet implementation, which is optimized for rapid lookup. Set has the same interface as Collection, so there isn’t any extra functionality like there is in the two different types of List. Instead, the Set is exactly a Collection—it just has different behavior. (This is the ideal use of inheritance and polymorphism: to express different behavior.) A Set determines membership based on the "value" of an object, a more complex topic that you will learn about in the Containers in Depth chapter. Here’s an example that uses a HashSet with Integer objects:
```java
//: holding/SetOfInteger.java
import java.util.*;
public class SetOfInteger {
public static void main(String[] args) {
Random rand = new Random(47);
Set<Integer> intset = new HashSet<Integer>();
for(int i = 0; i < 10000; i++)
intset.add(rand.nextInt(30));
System.out.println(intset);
}
} /* Output:
[15, 8, 23, 16, 7, 22, 9, 21, 6, 1, 29, 14, 24, 4, 19, 26, 11, 18, 3,
12, 27, 17, 2, 13, 28, 20, 25, 10, 5, 0]
*///:~
```
Ten thousand random numbers from o up to 29 are added to the Set, so you can imagine that each value has many duplications. And yet you can see that only one instance of each appears in the result. You’ll also notice that the output is in no discernible order. This is because a HashSet uses hashing for speed—hashing is covered in the Containers in Depth chapter. The order maintained by a HashSet is different from a TreeSet or a LinkedHashSet, since each implementation has a different way of storing elements. TreeSet keeps elements sorted into a red-black tree data structure, whereas HashSet uses the hashing function. LinkedHashSet also uses hashing for lookup speed, but appears to maintain elements in insertion order using a linked list. If you want the results to be sorted, one approach is to use a TreeSet instead of a HashSet:
```java
//: holding/SortedSetOfInteger.java
import java.util.*;
public class SortedSetOfInteger {
public static void main(String[] args) {
Random rand = new Random(47);
SortedSet<Integer> intset = new TreeSet<Integer>();
for(int i = 0; i < 10000; i++)
intset.add(rand.nextInt(30));
System.out.println(intset);
}
} /* Output:
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
*///:~
```
One of the most common operations you will perform is a test for set membership using contains( ), but there are also operations that will remind you of the Venn diagrams you may have been taught in elementary school:
```java
//: holding/SetOperations.java
import java.util.*;
import static net.mindview.util.Print.*;
public class SetOperations {
```

<!--p316-->
Holding Your Objects
```java
public static void main(String[] args) {
Set<String> set1 = new HashSet<String>();
Collections.addAll(set1,
"A B C D E F G H I J K L".split(" "));
set1.add("M");
print("H: " + set1.contains("H"));
print("N: " + set1.contains("N"));
Set<String> set2 = new HashSet<String>();
Collections.addAll(set2, "H I J K L".split(" "));
print("set2 in set1: " + set1.containsAll(set2));
set1.remove("H");
print("set1: " + set1);
print("set2 in set1: " + set1.containsAll(set2));
set1.removeAll(set2);
print("set2 removed from set1: " + set1);
Collections.addAll(set1, "X Y Z".split(" "));
print("‘X Y Z’ added to set1: " + set1);
}
} /* Output:
H: true
N: false
set2 in set1: true
set1: [D, K, C, B, L, G, I, M, A, F, J, E]
set2 in set1: false
set2 removed from set1: [D, C, B, G, M, A, F, E]
‘X Y Z’ added to set1: [Z, D, C, B, G, M, A, F, Y, X, E]
*///:~
```
The method names are self-explanatory, and there are a few more that you will find in the JDK documentation. Producing a list of unique elements can be quite useful. For example, suppose you’d like to list all the words in the file SetOperations.java, above. Using the net.mindview.TextFile utility that will be introduced later in the book, you can open and read a file into a Set:
```java
//: holding/UniqueWords.java
import java.util.*;
import net.mindview.util.*;
public class UniqueWords {
public static void main(String[] args) {
Set<String> words = new TreeSet<String>(
new TextFile("SetOperations.java", "\\W+"));
System.out.println(words);
}
} /* Output:
[A, B, C, Collections, D, E, F, G, H, HashSet, I, J, K, L, M, N, Output,
Print, Set, SetOperations, String, X, Y, Z, add, addAll, added, args,
class, contains, containsAll, false, from, holding, import, in, java,
main, mindview, net, new, print, public, remove, removeAll, removed,
set1, set2, split, static, to, true, util, void]
*///:~
```

<!--p317-->
TextFile is inherited from List<String>. The TextFile constructor opens the file and breaks it into words according to the regular expression "\\W+", which means "one or more letters" (regular expressions are introduced in the Strings chapter). The result is handed to the TreeSet constructor, which adds the contents of the List to itself. Since it is a TreeSet, the result is sorted. In this case, the sorting is done lexicographically so that the uppercase and lowercase letters are in separate groups. If you’d like to sort it alphabetically, you can pass the String.CASE_INSENSITIVE_ORDER Comparator (a comparator is an object that establishes order) to the TreeSet constructor:
```java
//: holding/UniqueWordsAlphabetic.java
// Producing an alphabetic listing.
import java.util.*;
import net.mindview.util.*;
public class UniqueWordsAlphabetic {
public static void main(String[] args) {
Set<String> words =
new TreeSet<String>(String.CASE_INSENSITIVE_ORDER);
words.addAll(
new TextFile("SetOperations.java", "\\W+"));
System.out.println(words);
}
} /* Output:
[A, add, addAll, added, args, B, C, class, Collections, contains,
containsAll, D, E, F, false, from, G, H, HashSet, holding, I, import,
in, J, java, K, L, M, main, mindview, N, net, new, Output, Print,
public, remove, removeAll, removed, Set, set1, set2, SetOperations,
split, static, String, to, true, util, void, X, Y, Z]
*///:~
```
Comparators will be explored in detail in the Arrays chapter. Exercise 16:(5) Create a Set of the vowels. Working from UniqueWords.Java, count and display the number of vowels in each input word, and also display the total number of vowels in the input file.
## Map
The ability to map objects to other objects can be an immensely powerful way to solve programming problems. For example, consider a program to examine the randomness of Java’s Random class. Ideally, Random would produce a perfect distribution of numbers, but to test this you need to generate many random numbers and count the ones that fall in the various ranges. A Map easily solves the problem; in this case, the key is the number produced by Random, and the value is the number of times that number appears:
```java
//: holding/Statistics.java
// Simple demonstration of HashMap.
import java.util.*;
public class Statistics {
public static void main(String[] args) {
Random rand = new Random(47);
Map<Integer,Integer> m =
new HashMap<Integer,Integer>();
for(int i = 0; i < 10000; i++) {
// Produce a number between 0 and 20:
int r = rand.nextInt(20);
Integer freq = m.get(r);
m.put(r, freq == null ? 1 : freq + 1);
}
System.out.println(m);
}
} /* Output:
```

<!--p318-->
Holding Your Objects
```java
{15=497, 4=481, 19=464, 8=468, 11=531, 16=533, 18=478, 3=508, 7=471,
12=521, 17=509, 2=489, 13=506, 9=549, 6=519, 1=502, 14=477, 10=513,
5=503, 0=481}
*///:~
```
In main( ), autoboxing converts the randomly generated int into an Integer reference that can be used with the HashMap (you can’t use primitives with containers). The get( ) method returns null if the key is not already in the container (which means that this is the first time the number has been found). Otherwise, the get( ) method produces the associated Integer value for the key, which is incremented (again, autoboxing simplifies the expression but there are actually conversions to and from Integer taking place). Here’s an example that allows you to use a String description to look up Pet objects. It also shows how you can test a Map to see if it contains a key or a value with containsKey( ) and containsValue( ):
```java
//: holding/PetMap.java
import typeinfo.pets.*;
import java.util.*;
import static net.mindview.util.Print.*;
public class PetMap {
public static void main(String[] args) {
Map<String,Pet> petMap = new HashMap<String,Pet>();
petMap.put("My Cat", new Cat("Molly"));
petMap.put("My Dog", new Dog("Ginger"));
petMap.put("My Hamster", new Hamster("Bosco"));
print(petMap);
Pet dog = petMap.get("My Dog");
print(dog);
print(petMap.containsKey("My Dog"));
print(petMap.containsValue(dog));
}
} /* Output:
{My Cat=Cat Molly, My Hamster=Hamster Bosco, My Dog=Dog Ginger}
Dog Ginger
true
true
*///:~
```
Maps, like arrays and Collections, can easily be expanded to multiple dimensions; you simply make a Map whose values are Maps (and the values of those Maps can be other containers, even other Maps). Thus, it’s quite easy to combine containers to quickly produce powerful data structures. For example, suppose you are keeping track of people who have multiple pets—all you need is a Map<Person, List<Pet>>:

<!--p319-->
```java
//: holding/MapOfList.java
package holding;
import typeinfo.pets.*;
import java.util.*;
import static net.mindview.util.Print.*;
public class MapOfList {
public static Map<Person, List<? extends Pet>>
petPeople = new HashMap<Person, List<? extends Pet>>();
static {
petPeople.put(new Person("Dawn"),
Arrays.asList(new Cymric("Molly"),new Mutt("Spot")));
petPeople.put(new Person("Kate"),
Arrays.asList(new Cat("Shackleton"),
new Cat("Elsie May"), new Dog("Margrett")));
petPeople.put(new Person("Marilyn"),
Arrays.asList(
new Pug("Louie aka Louis Snorkelstein Dupree"),
new Cat("Stanford aka Stinky el Negro"),
new Cat("Pinkola")));
petPeople.put(new Person("Luke"),
Arrays.asList(new Rat("Fuzzy"), new Rat("Fizzy")));
petPeople.put(new Person("Isaac"),
Arrays.asList(new Rat("Freckly")));
}
public static void main(String[] args) {
print("People: " + petPeople.keySet());
print("Pets: " + petPeople.values());
for(Person person : petPeople.keySet()) {
print(person + " has:");
for(Pet pet : petPeople.get(person))
print(" " + pet);
}
}
} /* Output:
People: [Person Luke, Person Marilyn, Person Isaac, Person Dawn, Person
Kate]
Pets: [[Rat Fuzzy, Rat Fizzy], [Pug Louie aka Louis Snorkelstein Dupree,
Cat Stanford aka Stinky el Negro, Cat Pinkola], [Rat Freckly], [Cymric
Molly, Mutt Spot], [Cat Shackleton, Cat Elsie May, Dog Margrett]]
Person Luke has:
Rat Fuzzy
Rat Fizzy
Person Marilyn has:
Pug Louie aka Louis Snorkelstein Dupree
Cat Stanford aka Stinky el Negro
Cat Pinkola
Person Isaac has:
Rat Freckly
Person Dawn has:
Cymric Molly
Mutt Spot
Person Kate has:
Cat Shackleton
Cat Elsie May
Dog Margrett
*///:~
```

<!--p320-->
A Map can return a Set of its keys, a Collection of its values, or a Set of its pairs. The keySet( ) method produces a Set of all the keys in petPeople, which is used in the foreach statement to iterate through the Map. Exercise 17:(2) Take the Gerbil class in Exercise 1 and put it into a Map instead, associating each Gerbil’s name (e.g. "Fuzzy" or "Spot") as a String (the key) for each Gerbil (the value) you put in the table. Get an Iterator for the keySet( ) and use it to move through the Map, looking up the Gerbil for each key and printing out the key and telling the Gerbil to hop( ). Exercise 18:(3) Fill a HashMap with key-value pairs. Print the results to show ordering by hash code. Extract the pairs, sort by key, and place the result into a LinkedHashMap. Show that the insertion order is maintained. Exercise 19:(2) Repeat the previous exercise with a HashSet and LinkedHashSet. Holding Your Objects Exercise 20:(3) Modify Exercise 16 so that you keep a count of the occurrence of each vowel. Exercise 21:(3) Using a Map<String,Integer>, follow the form of UniqueWords.java to create a program that counts the occurrence of words in a file. Sort the results using Collections.sort( ) with a second argument of String.CASE_INSENSITIVE_ORDER (to produce an alphabetic sort), and display the result. Exercise 22:(5) Modify the previous exercise so that it uses a class containing a String and a count field to store each different word, and a Set of these objects to maintain the list of words. Exercise 23:(4) Starting with Statistics.java, create a program that runs the test repeatedly and looks to see if any one number tends to appear more than the others in the results. Exercise 24: (2)Fill a LinkedHashMap with String keys and objects of your choice. Now extract the pairs, sort them based on the keys, and reinsert them into the Map. Exercise 25:(3) Create a Map<String,ArrayList<Integer>>. Use net.mindview.TextFile to open a text file and read it in a word at a time (use "\\W+" as the second argument to the TextFile constructor). Count the words as you read them in, and for each word in the file, record in the ArrayList<Integer> the word count associated with that word—this is, in effect, the location in the file where that word was found. Exercise 26: (4) Take the resulting Map from the previous exercise and re-create the order of the words as they appeared in the original file.
## Queue
A queue is typically a “first-in, first-out" (FIFO) container. That is, you put things in at one end and pull them out at the other, and the order in which you put them in will be the same order in which they come out. Queues are commonly used as a way to reliably transfer objects from one area of a program to another. Queues are especially important in concurrent programming, as you will see in the Concurrency chapter, because they safely transfer objects from one task to another. LinkedList has methods to support queue behavior and it implements the Queue interface, so a LinkedList can be used as a Queue implementation. By upcasting a LinkedList to a Queue, this example uses the Queuespecific methods in the Queue interface:

<!--p321-->
```java
//: holding/QueueDemo.java
// Upcasting to a Queue from a LinkedList.
import java.util.*;
public class QueueDemo {
public static void printQ(Queue queue) {
while(queue.peek() != null)
System.out.print(queue.remove() + " ");
System.out.println();
}
public static void main(String[] args) {
Queue<Integer> queue = new LinkedList<Integer>();
Random rand = new Random(47);
for(int i = 0; i < 10; i++)
```
Holding Your Objects
```java
queue.offer(rand.nextInt(i + 10));
printQ(queue);
Queue<Character> qc = new LinkedList<Character>();
for(char c : "Brontosaurus".toCharArray())
qc.offer(c);
printQ(qc);
}
} /* Output:
8 1 1 1 5 14 3 1 0 1
B r o n t o s a u r u s
*///:~
```
offer( ) is one of the Queue-specific methods; it inserts an element at the tail of the queue if it can, or returns false. Both peek( ) and element( ) return the head of the queue without removing it, but peek( ) returns null if the queue is empty and element( ) throws NoSuchElementException. Both poll( ) and remove( ) remove and return the head of the queue, but poll( ) returns null if the queue is empty, while remove( ) throws NoSuchElementException. Autoboxing automatically converts the int result of nextInt( ) into the Integer object required by queue, and the char c into the Character object required by qc. The Queue interface narrows access to the methods of LinkedList so that only the appropriate methods are available, and you are thus less tempted to use LinkedList methods (here, you could actually cast queue back to a LinkedList, but you are at least discouraged from doing so). Notice that the Queue-specific methods provide complete and standalone functionality. That is, you can have a usable Queue without any of the methods that are in Collection, from which it is inherited. Exercise 27: (2) Write a class called Command that contains a String and has a method operation( ) that displays the String. Write a second class with a method that fills a Queue with Command objects and returns it. Pass the filled Queue to a method in a third class that consumes the objects in the Queue and calls their operation( ) methods.
## PriorityQueue

<!--p322-->
First-in, first-out (FIFO) describes the most typical queuing discipline. A queuing discipline is what decides, given a group of elements in the queue, which one goes next. First-in, first- out says that the next element should be the one that was waiting the longest. Apriority queue says that the element that goes next is the one with the greatest need (the highest priority). For example, in an airport, a customer might be pulled out of a queue if their plane is about to leave. If you build a messaging system, some messages will be more important than others, and should be dealt with sooner, regardless of when they arrive. The PriorityQueue was added in Java SE5 to provide an automatic implementation for this behavior. When you offer( ) an object onto a PriorityQueue, that object is sorted into the queue.5 The default sorting uses the natural order of the objects in the queue, but you can modify the order by providing your own Comparator. The PriorityQueue ensures that when you call peek( ), poll( ) or remove( ), the element you get will be the one with the highest priority. 5This actually depends on the implementation. Priority queue algorithms typically sort on insertion (maintaining a heap), but they may also perform the selection of the most important element upon removal. The choice of algorithm could be important if object priority can change while it is waiting in the queue. It’s trivial to make a PriorityQueue that works with built-in types like Integer, String or Character. In the following example, the first set of values are the identical random values from the previous example, so you can see that they emerge differently from the PriorityQueue:
```java
//: holding/PriorityQueueDemo.java
import java.util.*;
public class PriorityQueueDemo {
public static void main(String[] args) {
PriorityQueue<Integer> priorityQueue =
new PriorityQueue<Integer>();
Random rand = new Random(47);
for(int i = 0; i < 10; i++)
priorityQueue.offer(rand.nextInt(i + 10));
QueueDemo.printQ(priorityQueue);
List<Integer> ints = Arrays.asList(25, 22, 20,
18, 14, 9, 3, 1, 1, 2, 3, 9, 14, 18, 21, 23, 25);
priorityQueue = new PriorityQueue<Integer>(ints);
QueueDemo.printQ(priorityQueue);
priorityQueue = new PriorityQueue<Integer>(
ints.size(), Collections.reverseOrder());
priorityQueue.addAll(ints);
QueueDemo.printQ(priorityQueue);
String fact = "EDUCATION SHOULD ESCHEW OBFUSCATION";
List<String> strings = Arrays.asList(fact.split(""));
PriorityQueue<String> stringPQ =
new PriorityQueue<String>(strings);
QueueDemo.printQ(stringPQ);
stringPQ = new PriorityQueue<String>(
strings.size(), Collections.reverseOrder());
stringPQ.addAll(strings);
QueueDemo.printQ(stringPQ);
Set<Character> charSet = new HashSet<Character>();
for(char c : fact.toCharArray())
charSet.add(c); // Autoboxing
PriorityQueue<Character> characterPQ =
new PriorityQueue<Character>(charSet);
QueueDemo.printQ(characterPQ);
}
} /* Output:
0 1 1 1 1 1 3 5 8 14
1 1 2 3 3 9 9 14 14 18 18 20 21 22 23 25 25
25 25 23 22 21 20 18 18 14 14 9 9 3 3 2 1 1
A A B C C C D D E E E F H H I I L N N O O O O S S S T T U U U W
W U U U T T S S S O O O O N N L I I H H F E E E D D C C C B A A
A B C D E F H I L N O S T U W
*///:~
```

<!--p323-->
You can see that duplicates are allowed, and the lowest values have the highest priority (in the case of String, spaces also count as values and are higher in priority than letters). To show how you can change the ordering by providing your own Comparator object, the third constructor call to PriorityQueue<Integer> and the second call to PriorityQueue<String> use the reverse-order Comparator produced by Collections.reverseOrder( ) (added in Java SE5). The last section adds a HashSet to eliminate duplicate Characters, just to make things a little more interesting. Holding Your Objects Integer, String and Character work with PriorityQueue because these classes already have natural ordering built in. If you want you use your own class in a PriorityQueue, you must include additional functionality to produce natural ordering, or provide your own Comparator. There’s a more sophisticated example that demonstrates this in the Containers in Depth chapter. Exercise 28: (2)Fill a PriorityQueue (using offer( )) with Double values created using java.util.Random, then remove the elements using poll( ) and display them. Exercise 29: (2) Create a simple class that inherits from Object and contains no members, and show that you cannot successfully add multiple elements of that class to a PriorityQueue. This issue will be fully explained in the Containers in Depth chapter.
## Collection vs. Iterator
Collection is the root interface that describes what is common for all sequence containers. It might be thought of as an "incidental interface," one that appeared because of commonality between other interfaces. In addition, the java.utiLAbstractCollection class provides a default implementation for a Collection, so that you can create a new subtype of AbstractCollection without unnecessary code duplication. One argument for having an interface is that it allows you to create more generic code. By writing to an interface rather than an implementation, your code can be applied to more types of objects.6So if I write a method that takes a Collection, that method can be applied to any type that implements Collection—and this allows a new class to choose to implement Collection in order to be used with my method. It’s interesting to note, however, that the Standard C++ Library has no common base class for its containers—all commonality between containers is achieved through iterators. In Java, it might seem sensible to follow the C++ approach, and to express commonality between containers using an iterator rather than a Collection. However, the two approaches are bound together, since implementing Collection also means providing an iterator( ) method:
```java
//: holding/InterfaceVsIterator.java
import typeinfo.pets.*;
import java.util.*;
public class InterfaceVsIterator {
public static void display(Iterator<Pet> it) {
while(it.hasNext()) {
Pet p = it.next();
System.out.print(p.id() + ":" + p + " ");
}
System.out.println();
}
public static void display(Collection<Pet> pets) {
for(Pet p : pets)
System.out.print(p.id() + ":" + p + " ");
System.out.println();
}
public static void main(String[] args) {
List<Pet> petList = Pets.arrayList(8);
Set<Pet> petSet = new HashSet<Pet>(petList);
Map<String,Pet> petMap =
new LinkedHashMap<String,Pet>();
```

<!--p324-->
6Some people advocate the automatic creation of an interface for every possible combination of methods in a class— sometimes for every single class. I believe that an interface should have more meaning than a mechanical duplication of method combinations, so I tend to wait until I see the value added by an interface before creating one.
```java
String[] names = ("Ralph, Eric, Robin, Lacey, " +
"Britney, Sam, Spot, Fluffy").split(", ");
for(int i = 0; i < names.length; i++)
petMap.put(names[i], petList.get(i));
display(petList);
display(petSet);
display(petList.iterator());
display(petSet.iterator());
System.out.println(petMap);
System.out.println(petMap.keySet());
display(petMap.values());
display(petMap.values().iterator());
}
} /* Output:
0:Rat 1:Manx 2:Cymric 3:Mutt 4:Pug 5:Cymric 6:Pug 7:Manx
4:Pug 6:Pug 3:Mutt 1:Manx 5:Cymric 7:Manx 2:Cymric 0:Rat
0:Rat 1:Manx 2:Cymric 3:Mutt 4:Pug 5:Cymric 6:Pug 7:Manx
4:Pug 6:Pug 3:Mutt 1:Manx 5:Cymric 7:Manx 2:Cymric 0:Rat
{Ralph=Rat, Eric=Manx, Robin=Cymric, Lacey=Mutt, Britney=Pug,
Sam=Cymric, Spot=Pug, Fluffy=Manx}
[Ralph, Eric, Robin, Lacey, Britney, Sam, Spot, Fluffy]
0:Rat 1:Manx 2:Cymric 3:Mutt 4:Pug 5:Cymric 6:Pug 7:Manx
0:Rat 1:Manx 2:Cymric 3:Mutt 4:Pug 5:Cymric 6:Pug 7:Manx
*///:~
```
Both versions of display( ) work with Map objects as well as with subtypes of Collection, and both the Collection interface and the Iterator decouple the display( ) methods from knowing about the particular implementation of the underlying container. In this case the two approaches come up even. In fact, Collection pulls ahead a bit because it is Iterable, and so in the implementation of display(Collection) the foreach construct can be used, which makes the code a little cleaner. The use of Iterator becomes compelling when you implement a foreign class, one that is not a Collection, in which it would be difficult or annoying to make it implement the Collection interface. For example, if we create a Collection implementation by inheriting from a class that holds Pet objects, we must implement all the Collection methods, even if we don’t need to use them within the display( ) method. Although this can easily be accomplished by inheriting from AbstractCollection, you’re forced to implement iterator( ) anyway, along with size( ), in order to provide the methods that are not implemented by AbstractCollection, but that are used by the other methods in AbstractCollection:

<!--p325-->
```java
//: holding/CollectionSequence.java
import typeinfo.pets.*;
import java.util.*;
public class CollectionSequence
extends AbstractCollection<Pet> {
private Pet[] pets = Pets.createArray(8);
public int size() { return pets.length; }
public Iterator<Pet> iterator() {
return new Iterator<Pet>() {
private int index = 0;
public boolean hasNext() {
return index < pets.length;
}
public Pet next() { return pets[index++]; }
public void remove() { // Not implemented
throw new UnsupportedOperationException();
}
};
}
public static void main(String[] args) {
CollectionSequence c = new CollectionSequence();
InterfaceVsIterator.display(c);
InterfaceVsIterator.display(c.iterator());
}
} /* Output:
0:Rat 1:Manx 2:Cymric 3:Mutt 4:Pug 5:Cymric 6:Pug 7:Manx
0:Rat 1:Manx 2:Cymric 3:Mutt 4:Pug 5:Cymric 6:Pug 7:Manx
*///:~
```
The remove( ) method is an "optional operation," which you will learn about in the Containers in Depth chapter. Here, it’s not necessary to implement it, and if you call it, it will throw an exception. From this example, you can see that if you implement Collection, you also implement iterator( ), and just implementing iterator( ) alone requires only slightly less effort than inheriting from AbstractCoUection. However, if your class already inherits from another class, then you cannot also inherit from AbstractCollection. In that case, to implement Collection you’d have to implement all the methods in the interface. In this case it would be much easier to inherit and add the ability to create an iterator:
```java
//: holding/NonCollectionSequence.java
import typeinfo.pets.*;
import java.util.*;
class PetSequence {
protected Pet[] pets = Pets.createArray(8);
}
public class NonCollectionSequence extends PetSequence {
public Iterator<Pet> iterator() {
return new Iterator<Pet>() {
private int index = 0;
public boolean hasNext() {
return index < pets.length;
}
public Pet next() { return pets[index++]; }
public void remove() { // Not implemented
throw new UnsupportedOperationException();
}
};
}
public static void main(String[] args) {
NonCollectionSequence nc = new NonCollectionSequence();
InterfaceVsIterator.display(nc.iterator());
}
} /* Output:
0:Rat 1:Manx 2:Cymric 3:Mutt 4:Pug 5:Cymric 6:Pug 7:Manx
*///:~
```

<!--p326-->
Producing an Iterator is the least-coupled way of connecting a sequence to a method that consumes that sequence, and puts far fewer constraints on the sequence class than does implementing Collection. Exercise 30:(5) Modify CollectionSequence.java so that it does not inherit from AbstractCollection, but instead implements Collection. Holding Your Objects Foreach and iterators So far, the foreach syntax has been primarily used with arrays, but it also works with any Collection object. You’ve actually seen a few examples of this using ArrayList, but here’s a general proof:
```java
//: holding/ForEachCollections.java
// All collections work with foreach.
import java.util.*;
public class ForEachCollections {
public static void main(String[] args) {
Collection<String> cs = new LinkedList<String>();
Collections.addAll(cs,
"Take the long way home".split(" "));
for(String s : cs)
System.out.print("‘" + s + "‘ ");
}
} /* Output:
‘Take’ ‘the’ ‘long’ ‘way’ ‘home’
*///:~
```
Since cs is a Collection, this code shows that working with foreach is a characteristic of all Collection objects. The reason that this works is that Java SE5 introduced a new interface called Iterable which contains an iterator( ) method to produce an Iterator, and the Iterable interface is what foreach uses to move through a sequence. So if you create any class that implements Iterable, you can use it in a foreach statement:

<!--p327-->
```java
//: holding/IterableClass.java
// Anything Iterable works with foreach.
import java.util.*;
public class IterableClass implements Iterable<String> {
protected String[] words = ("And that is how " +
"we know the Earth to be banana-shaped.").split(" ");
public Iterator<String> iterator() {
return new Iterator<String>() {
private int index = 0;
public boolean hasNext() {
return index < words.length;
}
public String next() { return words[index++]; }
public void remove() { // Not implemented
throw new UnsupportedOperationException();
}
};
}
public static void main(String[] args) {
for(String s : new IterableClass())
System.out.print(s + " ");
}
} /* Output:
And that is how we know the Earth to be banana-shaped.
*///:~
```
Holding Your Objects The iterator( ) method returns an instance of an anonymous inner implementation of Iterator<String> which delivers each word in the array. In main( ), you can see that IterableClass does indeed work in a foreach statement. In Java SE5, a number of classes have been made Iterable, primarily all Collection classes (but not Maps). For example, this code displays all the operating system environment variables:
```java
//: holding/EnvironmentVariables.java
import java.util.*;
public class EnvironmentVariables {
public static void main(String[] args) {
for(Map.Entry entry: System.getenv().entrySet()) {
System.out.println(entry.getKey() + ": " +
entry.getValue());
}
}
} /* (Execute to see output) *///:~
```
System.getenv( )7 returns a Map, entrySet( ) produces a Set of Map.Entry elements, and a Set is Iterable so it can be used in a foreach loop. A foreach statement works with an array or anything Iterable, but that doesn’t mean that an array is automatically an Iterable, nor is there any autoboxing that takes place:
```java
//: holding/ArrayIsNotIterable.java
import java.util.*;
public class ArrayIsNotIterable {
static <T> void test(Iterable<T> ib) {
for(T t : ib)
System.out.print(t + " ");
}
public static void main(String[] args) {
test(Arrays.asList(1, 2, 3));
String[] strings = { "A", "B", "C" };
// An array works in foreach, but it’s not Iterable:
//! test(strings);
// You must explicitly convert it to an Iterable:
test(Arrays.asList(strings));
}
} /* Output:
1 2 3 A B C
*///:~
```

<!--p328-->
Trying to pass an array as an Iterable argument fails. There is no automatic conversion to an Iterable;you must do it by hand. Exercise 31:(3) Modify polymorphism/shape/RandomShapeGenerator.java to make it Iterable. You’ll need to add a constructor that takes the number of elements that you want the iterator to produce before stopping. Verify that it works. 7This was not available before Java SE5, because it was thought to be too tightly coupled to the operating system, and thus to violate "write once, run anywhere." The fact that it is included now suggests that the Java designers are becoming more pragmatic. The Adapter Method idiom What if you have an existing class that is Iterable, and you’d like to add one or more new ways to use this class in a foreach statement? For example, suppose you’d like to choose whether to iterate through a list of words in either a forward or reverse direction. If you simply inherit from the class and override the iterator( ) method, you replace the existing method and you don’t get a choice. One solution is what I call the Adapter Method idiom. The "Adapter" part comes from design patterns, because you must provide a particular interface to satisfy the foreach statement. When you have one interface and you need another one, writing an adapter solves the problem. Here, I want to add the ability to produce a reverse iterator to the default forward iterator, so I can’t override. Instead, I add a method that produces an Iterable object which can then be used in the foreach statement. As you see here, this allows us to provide multiple ways to use foreach:
```java
//: holding/AdapterMethodIdiom.java
// The "Adapter Method" idiom allows you to use foreach
// with additional kinds of Iterables.
import java.util.*;
class ReversibleArrayList<T> extends ArrayList<T> {
public ReversibleArrayList(Collection<T> c) { super(c); }
public Iterable<T> reversed() {
return new Iterable<T>() {
public Iterator<T> iterator() {
return new Iterator<T>() {
int current = size() - 1;
public boolean hasNext() { return current > -1; }
public T next() { return get(current--); }
public void remove() { // Not implemented
throw new UnsupportedOperationException();
}
};
}
};
}
}
public class AdapterMethodIdiom {
public static void main(String[] args) {
ReversibleArrayList<String> ral =
new ReversibleArrayList<String>(
Arrays.asList("To be or not to be".split(" ")));
// Grabs the ordinary iterator via iterator():
for(String s : ral)
System.out.print(s + " ");
System.out.println();
// Hand it the Iterable of your choice
for(String s : ral.reversed())
System.out.print(s + " ");
}
} /* Output:
To be or not to be
be to not or be To
*///:~
```

<!--p329-->
If you simply put the ral object in the foreach statement, you get the (default) forward iterator. But if you call reversed( ) on the object, it produces different behavior. Using this approach, I can add two adapter methods to the IterableClass.java example:
```java
//: holding/MultiIterableClass.java
// Adding several Adapter Methods.
import java.util.*;
public class MultiIterableClass extends IterableClass {
public Iterable<String> reversed() {
return new Iterable<String>() {
public Iterator<String> iterator() {
return new Iterator<String>() {
int current = words.length - 1;
public boolean hasNext() { return current > -1; }
public String next() { return words[current--]; }
public void remove() { // Not implemented
throw new UnsupportedOperationException();
}
};
}
};
}
public Iterable<String> randomized() {
return new Iterable<String>() {
public Iterator<String> iterator() {
List<String> shuffled =
new ArrayList<String>(Arrays.asList(words));
Collections.shuffle(shuffled, new Random(47));
return shuffled.iterator();
}
};
}
public static void main(String[] args) {
MultiIterableClass mic = new MultiIterableClass();
for(String s : mic.reversed())
System.out.print(s + " ");
System.out.println();
for(String s : mic.randomized())
System.out.print(s + " ");
System.out.println();
for(String s : mic)
System.out.print(s + " ");
}
} /* Output:
banana-shaped. be to Earth the know we how is that And
is banana-shaped. Earth that how the be And we know to
And that is how we know the Earth to be banana-shaped.
*///:~
```
Notice that the second method, random( ), doesn’t create its own Iterator but simply returns the one from the shuffled List. You can see from the output that the Collections.shuffle( ) method doesn’t affect the original array, but only shuffles the references in shuffled. This is only true because the randomized( ) method wraps an ArrayList around the result of Arrays.asList( ). If the List produced by Arrays.asList( ) is shuffled directly, it will modify the underlying array, as you can see here:
```java
//: holding/ModifyingArraysAsList.java
import java.util.*;
public class ModifyingArraysAsList {
public static void main(String[] args) {
```

<!--p330-->
Holding Your Objects
```java
Random rand = new Random(47);
Integer[] ia = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
List<Integer> list1 =
new ArrayList<Integer>(Arrays.asList(ia));
System.out.println("Before shuffling: " + list1);
Collections.shuffle(list1, rand);
System.out.println("After shuffling: " + list1);
System.out.println("array: " + Arrays.toString(ia));
List<Integer> list2 = Arrays.asList(ia);
System.out.println("Before shuffling: " + list2);
Collections.shuffle(list2, rand);
System.out.println("After shuffling: " + list2);
System.out.println("array: " + Arrays.toString(ia));
}
} /* Output:
Before shuffling: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
After shuffling: [4, 6, 3, 1, 8, 7, 2, 5, 10, 9]
array: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Before shuffling: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
After shuffling: [9, 1, 6, 3, 7, 2, 5, 10, 4, 8]
array: [9, 1, 6, 3, 7, 2, 5, 10, 4, 8]
*///:~
```

<!--p331-->
In the first case, the output of Arrays.asList( ) is handed to the ArrayList( ) constructor, and this creates an ArrayList that references the elements of ia. Shuffling these references doesn’t modify the array. However, if you use the result of Arrays.asList(ia) directly, shuffling modifies the order of ia. It’s important to be aware that Arrays.asList( ) produces a List object that uses the underlying array as its physical implementation. If you do anything to that List that modifies it, and you don’t want the original array modified, you should make a copy into another container. Exercise 32:(2) Following the example of MultilterableClass, add reversed( ) and randomized( ) methods to NonCollectionSequence.java, as well as making NonCollectionSequence implement Iterable, and show that all the approaches work in foreach statements. Summary Java provides a number of ways to hold objects: 1.An array associates numerical indexes to objects. It holds objects of a known type so that you don’t have to cast the result when you’re looking up an object. It can be multidimensional, and it can hold primitives. However, its size cannot be changed once you create it. 2.A Collection holds single elements, and a Map holds associated pairs. With Java generics, you specify the type of object to be held in the containers, so you can’t put the wrong type into a container and you don’t have to cast elements when you fetch them out of a container. Both Collectionsand Mapsautomatically resize themselves as you add more elements. A container won’t hold primitives, but autoboxing takes care of translating primitives back and forth to the wrapper types held in the container. 3.Like an array, a List also associates numerical indexes to objects— thus, arrays and Lists are ordered containers. 4.Use an ArrayList if you’re doing a lot of random accesses, but a LinkedList if you will be doing a lot of insertions and removals in the middle of the list. 5.The behavior of Queues and stacks is provided via the LinkedList. 6.A Map is a way to associate not integral values, but objects with other objects. HashMapsare designed for rapid access, whereas a TreeMap keeps its keys in sorted order, and thus is not as fast as a HashMap. A LinkedHashMap keeps its elements in insertion order, but provides rapid access with hashing. 7.A Set only accepts one of each type of object. HashSets provide maximally fast lookups, whereas TreeSetskeep the elements in sorted order. LinkedHashSets keep elements in insertion order. 8.There’s no need to use the legacy classes Vector, Hashtable, and Stack in new code. It’s helpful to look at a simplified diagram of the Java containers (without the abstract classes or legacy components). This only includes the interfaces and classes that you will encounter on a regular basis. Simple Container Taxonomy You’ll see that there are really only four basic container components—Map, List, Set, and Queue—and only two or three implementations of each one (the java.util.concurrent implementations of Queue are not included in this diagram). The containers that you will use most often have heavy black lines around them. The dotted boxes represent interfaces, and the solid boxes are regular (concrete) classes. The dotted lines with hollow arrows indicate that a particular class is implementing an interface. The solid arrows show that a class can produce objects of the class the arrow is pointing to. For example, any Collection can produce an Iterator, and a List can produce a ListIterator (as well as an ordinary Iterator, since List is inherited from Collection). Here’s an example that shows the difference in methods between the various classes. The actual code is from the Generics chapter; I’m just calling it here to produce the output. The output also shows the interfaces that are implemented in each class or interface:
```java
//: holding/ContainerMethods.java
import net.mindview.util.*;
```

<!--p332-->
Holding Your Objects
```java
public class ContainerMethods {
public static void main(String[] args) {
ContainerMethodDifferences.main(args);
}
} /* Output: (Sample)
Collection: [add, addAll, clear, contains, containsAll, equals,
hashCode, isEmpty, iterator, remove, removeAll, retainAll, size,
toArray]
Interfaces in Collection: [Iterable]
Set extends Collection, adds: []
Interfaces in Set: [Collection]
HashSet extends Set, adds: []
Interfaces in HashSet: [Set, Cloneable, Serializable]
LinkedHashSet extends HashSet, adds: []
Interfaces in LinkedHashSet: [Set, Cloneable, Serializable]
TreeSet extends Set, adds: [pollLast, navigableHeadSet,
descendingIterator, lower, headSet, ceiling, pollFirst, subSet,
navigableTailSet, comparator, first, floor, last, navigableSubSet,
higher, tailSet]
Interfaces in TreeSet: [NavigableSet, Cloneable, Serializable]
List extends Collection, adds: [listIterator, indexOf, get, subList,
set, lastIndexOf]
Interfaces in List: [Collection]
ArrayList extends List, adds: [ensureCapacity, trimToSize]
Interfaces in ArrayList: [List, RandomAccess, Cloneable, Serializable]
LinkedList extends List, adds: [pollLast, offer, descendingIterator,
addFirst, peekLast, removeFirst, peekFirst, removeLast, getLast,
pollFirst, pop, poll, addLast, removeFirstOccurrence, getFirst, element,
peek, offerLast, push, offerFirst, removeLastOccurrence]
Interfaces in LinkedList: [List, Deque, Cloneable, Serializable]
Queue extends Collection, adds: [offer, element, peek, poll]
Interfaces in Queue: [Collection]
PriorityQueue extends Queue, adds: [comparator]
Interfaces in PriorityQueue: [Serializable]
Map: [clear, containsKey, containsValue, entrySet, equals, get,
hashCode, isEmpty, keySet, put, putAll, remove, size, values]
HashMap extends Map, adds: []
Interfaces in HashMap: [Map, Cloneable, Serializable]
LinkedHashMap extends HashMap, adds: []
Interfaces in LinkedHashMap: [Map]
SortedMap extends Map, adds: [subMap, comparator, firstKey, lastKey,
headMap, tailMap]
Interfaces in SortedMap: [Map]
TreeMap extends Map, adds: [descendingEntrySet, subMap, pollLastEntry,
lastKey, floorEntry, lastEntry, lowerKey, navigableHeadMap,
navigableTailMap, descendingKeySet, tailMap, ceilingEntry, higherKey,
pollFirstEntry, comparator, firstKey, floorKey, higherEntry, firstEntry,
navigableSubMap, headMap, lowerEntry, ceilingKey]
Interfaces in TreeMap: [NavigableMap, Cloneable, Serializable]
*///:~
```

<!--p333-->
You can see that all Sets except TreeSet have exactly the same interface as Collection. List and Collection differ significantly, although List requires methods that are in Collection. On the other hand, the methods in the Queue interface stand alone; the Collection methods are not required to create a functioning Queue implementation. Finally, the only intersection between Map and Collection is the fact that a Map can produce Collections using the entrySet( ) and values( ) methods. Notice the tagging interface java.util.RandomAccess, which is attached to ArrayList but not to LinkedList. This provides information for algorithms that might want to dynamically change their behavior depending on the use of a particular List. Holding Your Objects It’s true that this organization is somewhat odd, as object-oriented hierarchies go. However, as you learn more about the containers in java.util (in particular, in the Containers in Depth chapter), you’ll see that there are more issues than just a slightly odd inheritance structure. Container libraries have always been difficult design problems—solving these problems involves satisfying a set of forces that often oppose each other. So you should be prepared for some compromises here and there. Despite these issues, the Java containers are fundamental tools that you can use on a day-to-day basis to make your programs simpler, more powerful, and more effective. It might take you a little while to get comfortable with some aspects of the library, but I think you’ll find yourself rapidly acquiring and using the classes in this library. Solutions to selected exercises can be found in the electronic document The Thinking in Java Annotated Solution Guide, available for sale from www.MindView.net.