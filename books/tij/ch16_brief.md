# 16. Arrays (printed p535-566)


<!--p557-->
Arrays At the end of the Initialization & Cleanup chapter, you learned how to define and initialize an array. The simple view of arrays is that you create and populate them, you select elements from them using int indexes, and they don’t change their size. Most of the time that’s all you need to know, but sometimes you need to perform more sophisticated operations on arrays, and you may also need to evaluate the use of an array vs. a more flexible container. This chapter will show you how to think about arrays in more depth. Why arrays are special There are a number of other ways to hold objects, so what makes an array special? There are three issues that distinguish arrays from other types of containers: efficiency, type, and the ability to hold primitives. The array is Java’s most efficient way to store and randomly access a sequence of object references. The array is a simple linear sequence, which makes element access fast. The cost of this speed is that the size of an array object is fixed and cannot be changed for the lifetime of that array. You might suggest an ArrayList (from Holding Your Objects), which will automatically allocate more space, creating a new one and moving all the references from the old one to the new one. Although you should generally prefer an ArrayList to an array, this flexibility has overhead, so an ArrayList is measurably less efficient than an array. Both arrays and containers guarantee that you can’t abuse them. Whether you’re using an array or a container, you’ll get a RuntimeException if you exceed the bounds, indicating a programmer error. Before generics, the other container classes dealt with objects as if they had no specific type. That is, they treated them as type Object, the root class of all classes in Java. Arrays are superior to pre-generic containers because you create an array to hold a specific type. This means that you get compile-time type checking to prevent you from inserting the wrong type or mistaking the type that you’re extracting. Of course, Java will prevent you from sending an inappropriate message to an object at either compile time or run time. So it’s not riskier one way or the other; it’s just nicer if the compiler points it out to you, and there’s less likelihood that the end user will get surprised by an exception. An array can hold primitives, whereas a pre-generic container could not. With generics, however, containers can specify and check the type of objects they hold, and with autoboxing containers can act as if they are able to hold primitives, since the conversion is automatic. Here’s an example that compares arrays with generic containers:

<!--p558-->
```java
//: arrays/ContainerComparison.java
import java.util.*;
import static net.mindview.util.Print.*;
class BerylliumSphere {
private static long counter;
private final long id = counter++;
public String toString() { return "Sphere " + id; }
}
public class ContainerComparison {
public static void main(String[] args) {
BerylliumSphere[] spheres = new BerylliumSphere[10];
for(int i = 0; i < 5; i++)
spheres[i] = new BerylliumSphere();
print(Arrays.toString(spheres));
print(spheres[4]);
List<BerylliumSphere> sphereList =
new ArrayList<BerylliumSphere>();
for(int i = 0; i < 5; i++)
sphereList.add(new BerylliumSphere());
print(sphereList);
print(sphereList.get(4));
int[] integers = { 0, 1, 2, 3, 4, 5 };
print(Arrays.toString(integers));
print(integers[4]);
List<Integer> intList = new ArrayList<Integer>(
Arrays.asList(0, 1, 2, 3, 4, 5));
intList.add(97);
print(intList);
print(intList.get(4));
}
} /* Output:
[Sphere 0, Sphere 1, Sphere 2, Sphere 3, Sphere 4, null, null, null,
null, null]
Sphere 4
[Sphere 5, Sphere 6, Sphere 7, Sphere 8, Sphere 9]
Sphere 9
[0, 1, 2, 3, 4, 5]
[0, 1, 2, 3, 4, 5, 97]
*///:~
```

<!--p559-->
Both ways of holding objects are type-checked, and the only apparent difference is that arrays use [ ] for accessing elements, and a List uses methods such as add( ) and get( ). The similarity between arrays and the ArrayList is intentional, so that it’s conceptually easy to switch between the two. But as you saw in the Holding Your Objects chapter, containers have significantly more functionality than arrays. With the advent of autoboxing, containers are nearly as easy to use for primitives as arrays. The only remaining advantage to arrays is efficiency. However, when you’re solving a more general problem, arrays can be too restrictive, and in those cases you use a container class. Arrays are first-class objects Regardless of what type of array you’re working with, the array identifier is actually a reference to a true object that’s created on the heap. This is the object that holds the references to the other objects, and it can be created either implicitly, as part of the array initialization syntax, or explicitly with a new expression. Part of the array object (in fact, the only field or method you can access) is the read-only length member that tells you how many elements can be stored in that array object. The ‘[ ]’ syntax is the only other access that you have to the array object. The following example summarizes the various ways that an array can be initialized, and how the array references can be assigned to different array objects. It also shows that arrays of objects and arrays of primitives are almost identical in their use. The only difference is that arrays of objects hold references, but arrays of primitives hold the primitive values directly.
```java
//: arrays/ArrayOptions.java
// Initialization & re-assignment of arrays.
import java.util.*;
import static net.mindview.util.Print.*;
public class ArrayOptions {
public static void main(String[] args) {
// Arrays of objects:
BerylliumSphere[] a; // Local uninitialized variable
BerylliumSphere[] b = new BerylliumSphere[5];
// The references inside the array are
// automatically initialized to null:
print("b: " + Arrays.toString(b));
BerylliumSphere[] c = new BerylliumSphere[4];
for(int i = 0; i < c.length; i++)
if(c[i] == null) // Can test for null reference
c[i] = new BerylliumSphere();
// Aggregate initialization:
BerylliumSphere[] d = { new BerylliumSphere(),
new BerylliumSphere(), new BerylliumSphere()
};
// Dynamic aggregate initialization:
a = new BerylliumSphere[]{
new BerylliumSphere(), new BerylliumSphere(),
};
// (Trailing comma is optional in both cases)
print("a.length = " + a.length);
print("b.length = " + b.length);
print("c.length = " + c.length);
print("d.length = " + d.length);
a = d;
print("a.length = " + a.length);
// Arrays of primitives:
int[] e; // Null reference
int[] f = new int[5];
// The primitives inside the array are
// automatically initialized to zero:
print("f: " + Arrays.toString(f));
int[] g = new int[4];
for(int i = 0; i < g.length; i++)
g[i] = i*i;
int[] h = { 11, 47, 93 };
// Compile error: variable e not initialized:
//!print("e.length = " + e.length);
print("f.length = " + f.length);
print("g.length = " + g.length);
print("h.length = " + h.length);
e = h;
print("e.length = " + e.length);
e = new int[]{ 1, 2 };
print("e.length = " + e.length);
}
} /* Output:
b: [null, null, null, null, null]
a.length = 2
b.length = 5
c.length = 4
d.length = 3
a.length = 3
```

<!--p560-->
Arrays
```java
f: [0, 0, 0, 0, 0]
f.length = 5
g.length = 4
h.length = 3
e.length = 3
e.length = 2
*///:~
```
The array a is an uninitialized local variable, and the compiler prevents you from doing anything with this reference until you’ve properly initialized it. The array b is initialized to point to an array of BerylliumSphere references, but no actual BerylliumSphere objects are ever placed in that array. However, you can still ask what the size of the array is, since b is pointing to a legitimate object. This brings up a slight drawback: You can’t find out how many elements are actually in the array, since length tells you only how many elements can be placed in the array; that is, the size of the array object, not the number of elements it actually holds. However, when an array object is created, its references are automatically initialized to null, so you can see whether a particular array slot has an object in it by checking to see whether it’s null. Similarly, an array of primitives is automatically initialized to zero for numeric types, (char)o for char, and false for boolean. Array c shows the creation of the array object followed by the assignment of BerylliumSphere objects to all the slots in the array. Array d shows the "aggregate initialization" syntax that causes the array object to be created (implicitly with new on the heap, just like for array c) and initialized with BerylliumSphere objects, all in one statement. The next array initialization can be thought of as a "dynamic aggregate initialization." The aggregate initialization used by d must be used at the point of d’s definition, but with the second syntax you can create and initialize an array object anywhere. For example, suppose hide( ) is a method that takes an array of BerylliumSphere objects. You could call it by saying:
```java
hide(d);
```
but you can also dynamically create the array you want to pass as the argument:
```java
hide(new BerylliumSphere[]{ new BerylliumSphere(),
new BerylliumSphere() });
```
In many situations this syntax provides a more convenient way to write code. The expression:
```java
a = d;
```

<!--p561-->
shows how you can take a reference that’s attached to one array object and assign it to another array object, just as you can do with any other type of object reference. Now both a and d are pointing to the same array object on the heap. The second part of ArrayOptions.java shows that primitive arrays work just like object arrays except that primitive arrays hold the primitive values directly. Exercise 1:(2) Create a method that takes an array of BerylliumSphere as an argument. Call the method, creating the argument dynamically. Demonstrate that ordinary aggregate array initialization doesn’t work in this case. Discover the only situations where ordinary aggregate array initialization works, and where dynamic aggregate initialization is redundant. Returning an array Suppose you’re writing a method and you don’t want to return just one thing, but a whole bunch of things. Languages like C and C++ make this difficult because you can’t just return an array, only a pointer to an array. This introduces problems because it becomes messy to control the lifetime of the array, which leads to memory leaks. In Java, you just return the array. You never worry about responsibility for that array—it will be around as long as you need it, and the garbage collector will clean it up when you’re done. As an example, consider returning an array of String:
```java
//: arrays/IceCream.java
// Returning arrays from methods.
import java.util.*;
public class IceCream {
private static Random rand = new Random(47);
static final String[] FLAVORS = {
"Chocolate", "Strawberry", "Vanilla Fudge Swirl",
"Mint Chip", "Mocha Almond Fudge", "Rum Raisin",
"Praline Cream", "Mud Pie"
};
public static String[] flavorSet(int n) {
if(n > FLAVORS.length)
throw new IllegalArgumentException("Set too big");
String[] results = new String[n];
boolean[] picked = new boolean[FLAVORS.length];
for(int i = 0; i < n; i++) {
int t;
do
t = rand.nextInt(FLAVORS.length);
while(picked[t]);
results[i] = FLAVORS[t];
picked[t] = true;
}
return results;
}
public static void main(String[] args) {
for(int i = 0; i < 7; i++)
System.out.println(Arrays.toString(flavorSet(3)));
}
} /* Output:
[Rum Raisin, Mint Chip, Mocha Almond Fudge]
[Chocolate, Strawberry, Mocha Almond Fudge]
[Strawberry, Mint Chip, Mocha Almond Fudge]
[Rum Raisin, Vanilla Fudge Swirl, Mud Pie]
[Vanilla Fudge Swirl, Chocolate, Mocha Almond Fudge]
[Praline Cream, Strawberry, Mocha Almond Fudge]
[Mocha Almond Fudge, Strawberry, Mint Chip]
*///:~
```

<!--p562-->
The method flavorSet( ) creates an array of String called results. The size of this array is n, determined by the argument that you pass into the method. Then it proceeds to choose flavors randomly from the array FLAVORS and place them into results, which it returns. Returning an array is just like returning any other object—it’s a reference. It’s not important that the array was created within flavorSet( ), or that the array was created anyplace else, for that matter. The garbage collector takes care of cleaning up the array when you’re done with it, and the array will persist for as long as you need it. Arrays As an aside, notice that when flavorSet( ) chooses flavors randomly, it ensures that a particular choice hasn’t already been selected. This is performed in a do loop that keeps making random choices until it finds one not already in the picked array. (Of course, a String comparison also could have been performed to see if the random choice was already in the results array.) If it’s successful, it adds the entry and finds the next one (i gets incremented). You can see from the output that flavorSet( ) chooses the flavors in a random order each time. Exercise 2:(1) Write a method that takes an int argument and returns an array of that size, filled with BerylliumSphere objects. Multidimensional arrays You can easily create multidimensional arrays. For a multidimensional array of primitives, you delimit each vector in the array by using curly braces:
```java
//: arrays/MultidimensionalPrimitiveArray.java
// Creating multidimensional arrays.
import java.util.*;
public class MultidimensionalPrimitiveArray {
public static void main(String[] args) {
int[][] a = {
{ 1, 2, 3, },
{ 4, 5, 6, },
};
System.out.println(Arrays.deepToString(a));
}
} /* Output:
[[1, 2, 3], [4, 5, 6]]
*///:~
```
Each nested set of curly braces moves you into the next level of the array. This example uses the Java SE5 Arrays.deepToString( ) method, which turns multidimensional arrays into Strings, as you can see from the output. You can also allocate an array using new. Here’s a three-dimensional array allocated in a new expression:

<!--p563-->
```java
//: arrays/ThreeDWithNew.java
import java.util.*;
public class ThreeDWithNew {
public static void main(String[] args) {
// 3-D array with fixed length:
int[][][] a = new int[2][2][4];
System.out.println(Arrays.deepToString(a));
}
} /* Output:
[[[0, 0, 0, 0], [0, 0, 0, 0]], [[0, 0, 0, 0], [0, 0, 0, 0]]]
*///:~
```
You can see that primitive array values are automatically initialized if you don’t give them an explicit initialization value. Arrays of objects are initialized to null. Each vector in the arrays that make up the matrix can be of any length (this is called a ragged array):
```java
//: arrays/RaggedArray.java
import java.util.*;
public class RaggedArray {
public static void main(String[] args) {
Random rand = new Random(47);
// 3-D array with varied-length vectors:
int[][][] a = new int[rand.nextInt(7)][][];
for(int i = 0; i < a.length; i++) {
a[i] = new int[rand.nextInt(5)][];
for(int j = 0; j < a[i].length; j++)
a[i][j] = new int[rand.nextInt(5)];
}
System.out.println(Arrays.deepToString(a));
}
} /* Output:
[[], [[0], [0], [0, 0, 0, 0]], [[], [0, 0], [0, 0]], [[0, 0, 0], [0],
[0, 0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0], []], [[0], [], [0]]]
*///:~
```
The first new creates an array with a random-length first element and the rest undetermined. The second new inside the for loop fills out the elements but leaves the third index undetermined until you hit the third new. You can deal with arrays of non-primitive objects in a similar fashion. Here, you can see how to collect many new expressions with curly braces:
```java
//: arrays/MultidimensionalObjectArrays.java
import java.util.*;
public class MultidimensionalObjectArrays {
public static void main(String[] args) {
BerylliumSphere[][] spheres = {
{ new BerylliumSphere(), new BerylliumSphere() },
{ new BerylliumSphere(), new BerylliumSphere(),
new BerylliumSphere(), new BerylliumSphere() },
{ new BerylliumSphere(), new BerylliumSphere(),
new BerylliumSphere(), new BerylliumSphere(),
new BerylliumSphere(), new BerylliumSphere(),
new BerylliumSphere(), new BerylliumSphere() },
};
System.out.println(Arrays.deepToString(spheres));
}
} /* Output:
[[Sphere 0, Sphere 1], [Sphere 2, Sphere 3, Sphere 4, Sphere 5], [Sphere
6, Sphere 7, Sphere 8, Sphere 9, Sphere 10, Sphere 11, Sphere 12, Sphere
13]]
*///:~
```

<!--p564-->
You can see that spheres is another ragged array, where the length of each list of objects is different. Arrays Autoboxing also works with array initializers:
```java
//: arrays/AutoboxingArrays.java
import java.util.*;
public class AutoboxingArrays {
public static void main(String[] args) {
Integer[][] a = { // Autoboxing:
{ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 },
{ 21, 22, 23, 24, 25, 26, 27, 28, 29, 30 },
{ 51, 52, 53, 54, 55, 56, 57, 58, 59, 60 },
{ 71, 72, 73, 74, 75, 76, 77, 78, 79, 80 },
};
System.out.println(Arrays.deepToString(a));
}
} /* Output:
[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [21, 22, 23, 24, 25, 26, 27, 28, 29,
30], [51, 52, 53, 54, 55, 56, 57, 58, 59, 60], [71, 72, 73, 74, 75, 76,
77, 78, 79, 80]]
*///:~
```
Here’s how an array of non-primitive objects can be built up piece-by-piece:
```java
//: arrays/AssemblingMultidimensionalArrays.java
// Creating multidimensional arrays.
import java.util.*;
public class AssemblingMultidimensionalArrays {
public static void main(String[] args) {
Integer[][] a;
a = new Integer[3][];
for(int i = 0; i < a.length; i++) {
a[i] = new Integer[3];
for(int j = 0; j < a[i].length; j++)
a[i][j] = i * j; // Autoboxing
}
System.out.println(Arrays.deepToString(a));
}
} /* Output:
[[0, 0, 0], [0, 1, 2], [0, 2, 4]]
*///:~
```
The i*j is only there to put an interesting value into the Integer. The Arrays.deepToString( ) method works with both primitive arrays and object arrays:

<!--p565-->
```java
//: arrays/MultiDimWrapperArray.java
// Multidimensional arrays of "wrapper" objects.
import java.util.*;
public class MultiDimWrapperArray {
public static void main(String[] args) {
Integer[][] a1 = { // Autoboxing
{ 1, 2, 3, },
{ 4, 5, 6, },
};
Double[][][] a2 = { // Autoboxing
{ { 1.1, 2.2 }, { 3.3, 4.4 } },
{ { 5.5, 6.6 }, { 7.7, 8.8 } },
{ { 9.9, 1.2 }, { 2.3, 3.4 } },
};
String[][] a3 = {
{ "The", "Quick", "Sly", "Fox" },
{ "Jumped", "Over" },
{ "The", "Lazy", "Brown", "Dog", "and", "friend" },
};
System.out.println("a1: " + Arrays.deepToString(a1));
System.out.println("a2: " + Arrays.deepToString(a2));
System.out.println("a3: " + Arrays.deepToString(a3));
}
} /* Output:
a1: [[1, 2, 3], [4, 5, 6]]
a2: [[[1.1, 2.2], [3.3, 4.4]], [[5.5, 6.6], [7.7, 8.8]], [[9.9, 1.2],
[2.3, 3.4]]]
a3: [[The, Quick, Sly, Fox], [Jumped, Over], [The, Lazy, Brown, Dog,
and, friend]]
*///:~
```
Again, in the Integer and Double arrays, Java SE5 autoboxing creates the wrapper objects for you. Exercise 3:(4) Write a method that creates and initializes a twodimensional array of double. The size of the array is determined by the arguments of the method, and the initialization values are a range determined by beginning and ending values that are also arguments of the method. Create a second method that will print the array generated by the first method. In main( ) test the methods by creating and printing several different sizes of arrays. Exercise 4:(2) Repeat the previous exercise for a three-dimensional array. Exercise 5:(1) Demonstrate that multidimensional arrays of nonprimitive types are automatically initialized to null. Exercise 6:(1) Write a method that takes two int arguments, indicating the two sizes of a 2-D array. The method should create and fill a 2-D array of BerylliumSphere according to the size arguments. Exercise 7:(1) Repeat the previous exercise for a 3-D array. Arrays and generics In general, arrays and generics do not mix well. You cannot instantiate arrays of parameterized types:
```java
Peel<Banana>[] peels = new Peel<Banana> [10]; // Illegal
```
Erasure removes the parameter type information, and arrays must know the exact type that they hold, in order to enforce type safety. However, you can parameterize the type of the array itself:
```java
//: arrays/ParameterizedArrayType.java
class ClassParameter<T> {
public T[] f(T[] arg) { return arg; }
```

<!--p566-->
Arrays
```java
}
class MethodParameter {
public static <T> T[] f(T[] arg) { return arg; }
}
public class ParameterizedArrayType {
public static void main(String[] args) {
Integer[] ints = { 1, 2, 3, 4, 5 };
Double[] doubles = { 1.1, 2.2, 3.3, 4.4, 5.5 };
Integer[] ints2 =
new ClassParameter<Integer>().f(ints);
Double[] doubles2 =
new ClassParameter<Double>().f(doubles);
ints2 = MethodParameter.f(ints);
doubles2 = MethodParameter.f(doubles);
}
} ///:~
```
Note the convenience of using a parameterized method instead of a parameterized class: You don’t have to instantiate a class with a parameter for each different type you need to apply it to, and you can make it static. Of course, you can’t always choose to use a parameterized method instead of a parameterized class, but it can be preferable. As it turns out, it’s not precisely correct to say that you cannot create arrays of generic types. True, the compiler won’t let you instantiate an array of a generic type. However, it will let you create a reference to such an array. For example:
```java
List<String>[] ls;
```
This passes through the compiler without complaint. And although you cannot create an actual array object that holds generics, you can create an array of the non-generified type and cast it:

<!--p567-->
```java
//: arrays/ArrayOfGenerics.java
// It is possible to create arrays of generics.
import java.util.*;
public class ArrayOfGenerics {
@SuppressWarnings("unchecked")
public static void main(String[] args) {
List<String>[] ls;
List[] la = new List[10];
ls = (List<String>[])la; // "Unchecked" warning
ls[0] = new ArrayList<String>();
// Compile-time checking produces an error:
//! ls[1] = new ArrayList<Integer>();
// The problem: List<String> is a subtype of Object
Object[] objects = ls; // So assignment is OK
// Compiles and runs without complaint:
objects[1] = new ArrayList<Integer>();
// However, if your needs are straightforward it is
// possible to create an array of generics, albeit
// with an "unchecked" warning:
List<BerylliumSphere>[] spheres =
(List<BerylliumSphere>[])new List[10];
for(int i = 0; i < spheres.length; i++)
spheres[i] = new ArrayList<BerylliumSphere>();
}
} ///:~
```
Once you have a reference to a List<String>[], you can see that you get some compile-time checking. The problem is that arrays are covariant, so a List<String>[] is also an Object[], and you can use this to assign an ArrayList<Integer> into your array, with no error at either compile time or run time. If you know you’re not going to upcast and your needs are relatively simple, however, it is possible to create an array of generics, which will provide basic compile-time type checking. However, a generic container will virtually always be a better choice than an array of generics. In general you’ll find that generics are effective at the boundaries of a class or method. In the interiors, erasure usually makes generics unusable. So you cannot, for example, create an array of a generic type:
```java
//: arrays/ArrayOfGenericType.java
// Arrays of generic types won’t compile.
public class ArrayOfGenericType<T> {
T[] array; // OK
@SuppressWarnings("unchecked")
public ArrayOfGenericType(int size) {
//! array = new T[size]; // Illegal
array = (T[])new Object[size]; // "unchecked" Warning
}
// Illegal:
//! public <U> U[] makeArray() { return new U[10]; }
} ///:~
```

<!--p568-->
Erasure gets in the way again—this example attempts to create arrays of types that have been erased, and are thus unknown types. Notice that you can create an array of Object, and cast it, but without the @SuppressWarnings annotation you get an "unchecked" warning at compile time because the array doesn’t really hold or dynamically check for type T. That is, if I create a String[], Java will enforce at both compile time and run time that I can only place String objects in that array. However, if I create an Object[], Ican put anything into that array except primitive types. Exercise 8:(1) Demonstrate the assertions in the previous paragraph. Exercise 9:(3) Create the classes necessary for the Peel<Banana> example and show that the compiler doesn’t accept it. Fix the problem using an ArrayList. Exercise 10: (2) Modify ArrayOfGenerics .Java to use containers instead of arrays. Show that you can eliminate the compile-time warnings. Arrays Creating test data When experimenting with arrays, and with programs in general, it’s helpful to be able to easily generate arrays filled with test data. The tools in this section will fill an array with values or objects.
## Arrays.fill()
The Java standard library Arrays class has a rather trivial fill( ) method: It only duplicates a single value into each location, or in the case of objects, copies the same reference into each location. Here’s an example:

<!--p569-->
```java
//: arrays/FillingArrays.java
// Using Arrays.fill()
import java.util.*;
import static net.mindview.util.Print.*;
public class FillingArrays {
public static void main(String[] args) {
int size = 6;
boolean[] a1 = new boolean[size];
byte[] a2 = new byte[size];
char[] a3 = new char[size];
short[] a4 = new short[size];
int[] a5 = new int[size];
long[] a6 = new long[size];
float[] a7 = new float[size];
double[] a8 = new double[size];
String[] a9 = new String[size];
Arrays.fill(a1, true);
print("a1 = " + Arrays.toString(a1));
Arrays.fill(a2, (byte)11);
print("a2 = " + Arrays.toString(a2));
Arrays.fill(a3, ‘x’);
print("a3 = " + Arrays.toString(a3));
Arrays.fill(a4, (short)17);
print("a4 = " + Arrays.toString(a4));
Arrays.fill(a5, 19);
print("a5 = " + Arrays.toString(a5));
Arrays.fill(a6, 23);
print("a6 = " + Arrays.toString(a6));
Arrays.fill(a7, 29);
print("a7 = " + Arrays.toString(a7));
Arrays.fill(a8, 47);
print("a8 = " + Arrays.toString(a8));
Arrays.fill(a9, "Hello");
print("a9 = " + Arrays.toString(a9));
// Manipulating ranges:
Arrays.fill(a9, 3, 5, "World");
print("a9 = " + Arrays.toString(a9));
}
} /* Output:
a1 = [true, true, true, true, true, true]
a2 = [11, 11, 11, 11, 11, 11]
a3 = [x, x, x, x, x, x]
a4 = [17, 17, 17, 17, 17, 17]
a5 = [19, 19, 19, 19, 19, 19]
a6 = [23, 23, 23, 23, 23, 23]
a7 = [29.0, 29.0, 29.0, 29.0, 29.0, 29.0]
```
Arrays
```java
a8 = [47.0, 47.0, 47.0, 47.0, 47.0, 47.0]
a9 = [Hello, Hello, Hello, Hello, Hello, Hello]
a9 = [Hello, Hello, Hello, World, World, Hello]
*///:~
```
You can either fill the entire array or, as the last two statements show, fill a range of elements. But since you can only call Arrays.fill( ) with a single data value, the results are not especially useful.
## Data Generators
To create more interesting arrays of data, but in a flexible fashion, we’ll use the Generator concept that was introduced in the Generics chapter. If a tool uses a Generator, you can produce any kind of data via your choice of Generator (this is an example of the Strategy design pattern—each different Generator represents a different strategy1). This section will supply some Generators, and as you’ve seen before, you can easily define your own. First, here’s a basic set of counting generators for all primitive wrapper types, and for Strings. The generator classes are nested within the CountingGenerator class so that they may use the same name as the object types they are generating; for example, a generator that creates Integer objects would be created with the expression new CountingGenerator.Integer( ):
```java
//: net/mindview/util/CountingGenerator.java
// Simple generator implementations.
package net.mindview.util;
public class CountingGenerator {
public static class
Boolean implements Generator<java.lang.Boolean> {
private boolean value = false;
public java.lang.Boolean next() {
value = !value; // Just flips back and forth
return value;
}
}
public static class
Byte implements Generator<java.lang.Byte> {
private byte value = 0;
public java.lang.Byte next() { return value++; }
}
static char[] chars = ("abcdefghijklmnopqrstuvwxyz" +
"ABCDEFGHIJKLMNOPQRSTUVWXYZ").toCharArray();
public static class
Character implements Generator<java.lang.Character> {
int index = -1;
public java.lang.Character next() {
index = (index + 1) % chars.length;
return chars[index];
}
}
public static class
String implements Generator<java.lang.String> {
private int length = 7;
```

<!--p570-->
1 Although this is a place where things are a bit fuzzy. You could also make an argument that a Generator represents the Command pattern. However, I think that the task is to fill an array, and the Generator fulfills part of that task, so it’s more strategy-like than command-like.
```java
Generator<java.lang.Character> cg = new Character();
public String() {}
public String(int length) { this.length = length; }
public java.lang.String next() {
char[] buf = new char[length];
for(int i = 0; i < length; i++)
buf[i] = cg.next();
return new java.lang.String(buf);
}
}
public static class
Short implements Generator<java.lang.Short> {
private short value = 0;
public java.lang.Short next() { return value++; }
}
public static class
Integer implements Generator<java.lang.Integer> {
private int value = 0;
public java.lang.Integer next() { return value++; }
}
public static class
Long implements Generator<java.lang.Long> {
private long value = 0;
public java.lang.Long next() { return value++; }
}
public static class
Float implements Generator<java.lang.Float> {
private float value = 0;
public java.lang.Float next() {
float result = value;
value += 1.0;
return result;
}
}
public static class
Double implements Generator<java.lang.Double> {
private double value = 0.0;
public java.lang.Double next() {
double result = value;
value += 1.0;
return result;
}
}
} ///:~
```
Each class implements some meaning of "counting." In the case of CountingGenerator.Character, this is just the upper and lowercase letters repeated over and over. The CountingGenerator.String class uses CountingGenerator.Character to fill an array of characters, which is then turned into a String. The size of the array is determined by the constructor argument. Notice that CountingGenerator.String uses a basic Generator <java.lang. Character > instead of a specific reference to CountingGenerator.Character. Later, this generator can be replaced to produce RandomGenerator.String in RandomGenerator.java. Here’s a test tool that uses reflection with the nested Generator idiom, so that it can be used to test any set of Generators that follow this form:

<!--p571-->
```java
//: arrays/GeneratorsTest.java
import net.mindview.util.*;
public class GeneratorsTest {
public static int size = 10;
public static void test(Class<?> surroundingClass) {
for(Class<?> type : surroundingClass.getClasses()) {
System.out.print(type.getSimpleName() + ": ");
try {
Generator<?> g = (Generator<?>)type.newInstance();
for(int i = 0; i < size; i++)
System.out.printf(g.next() + " ");
System.out.println();
} catch(Exception e) {
throw new RuntimeException(e);
}
}
}
public static void main(String[] args) {
test(CountingGenerator.class);
}
} /* Output:
Double: 0.0 1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 9.0
Float: 0.0 1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 9.0
Long: 0 1 2 3 4 5 6 7 8 9
Integer: 0 1 2 3 4 5 6 7 8 9
Short: 0 1 2 3 4 5 6 7 8 9
String: abcdefg hijklmn opqrstu vwxyzAB CDEFGHI JKLMNOP QRSTUVW XYZabcd
efghijk lmnopqr
Character: a b c d e f g h i j
Byte: 0 1 2 3 4 5 6 7 8 9
Boolean: true false true false true false true false true false
*///:~
```
This assumes that the class under test contains a set of nested Generator objects, each of which has a default constructor (one without arguments). The reflection method getClasses( ) produces all the nested classes. The test( ) method then creates an instance of each of these generators, and prints the result produced by calling next( ) ten times. Here is a set of Generators that use the random number generator. Because the Random constructor is initialized with a constant value, the output is repeatable each time you run a program using one of these Generators:
```java
//: net/mindview/util/RandomGenerator.java
// Generators that produce random values.
package net.mindview.util;
import java.util.*;
public class RandomGenerator {
private static Random r = new Random(47);
public static class
Boolean implements Generator<java.lang.Boolean> {
public java.lang.Boolean next() {
return r.nextBoolean();
}
}
public static class
Byte implements Generator<java.lang.Byte> {
public java.lang.Byte next() {
return (byte)r.nextInt();
}
}
public static class
Character implements Generator<java.lang.Character> {
public java.lang.Character next() {
return CountingGenerator.chars[
r.nextInt(CountingGenerator.chars.length)];
```

<!--p572-->
Arrays
```java
}
}
public static class
String extends CountingGenerator.String {
// Plug in the random Character generator:
{ cg = new Character(); } // Instance initializer
public String() {}
public String(int length) { super(length); }
}
public static class
Short implements Generator<java.lang.Short> {
public java.lang.Short next() {
return (short)r.nextInt();
}
}
public static class
Integer implements Generator<java.lang.Integer> {
private int mod = 10000;
public Integer() {}
public Integer(int modulo) { mod = modulo; }
public java.lang.Integer next() {
return r.nextInt(mod);
}
}
public static class
Long implements Generator<java.lang.Long> {
private int mod = 10000;
public Long() {}
public Long(int modulo) { mod = modulo; }
public java.lang.Long next() {
return new java.lang.Long(r.nextInt(mod));
}
}
public static class
Float implements Generator<java.lang.Float> {
public java.lang.Float next() {
// Trim all but the first two decimal places:
int trimmed = Math.round(r.nextFloat() * 100);
return ((float)trimmed) / 100;
}
}
public static class
Double implements Generator<java.lang.Double> {
public java.lang.Double next() {
long trimmed = Math.round(r.nextDouble() * 100);
return ((double)trimmed) / 100;
}
}
} ///:~
```
You can see that RandomGenerator.String inherits from CountingGenerator.String and simply plugs in the new Character generator. To generate numbers that aren’t too large, RandomGenerator.Integer defaults to a modulus of 10,000, but the overloaded constructor allows you to choose a smaller value. The same approach is used for RandomGenerator.Long. For the Float and Double Generators, the values after the decimal point are trimmed. We can reuse GeneratorsTest to test RandomGenerator:

<!--p573-->
```java
//: arrays/RandomGeneratorsTest.java
import net.mindview.util.*;
public class RandomGeneratorsTest {
public static void main(String[] args) {
GeneratorsTest.test(RandomGenerator.class);
}
} /* Output:
Double: 0.73 0.53 0.16 0.19 0.52 0.27 0.26 0.05 0.8 0.76
Float: 0.53 0.16 0.53 0.4 0.49 0.25 0.8 0.11 0.02 0.8
Long: 7674 8804 8950 7826 4322 896 8033 2984 2344 5810
Integer: 8303 3141 7138 6012 9966 8689 7185 6992 5746 3976
Short: 3358 20592 284 26791 12834 -8092 13656 29324 -1423 5327
String: bkInaMe sbtWHkj UrUkZPg wsqPzDy CyRFJQA HxxHvHq XumcXZJ oogoYWM
NvqeuTp nXsgqia
Character: x x E A J J m z M s
Byte: -60 -17 55 -14 -5 115 39 -37 79 115
Boolean: false true false false true true true true true true
*///:~
```
You can change the number of values produced by changing the GeneratorsTest.size value, which is public.
## Creating arrays from Generators
In order to take a Generator and produce an array, we need two conversion tools. The first one uses any Generator to produce an array of Object subtypes. To cope with the problem of primitives, the second tool takes any array of primitive wrapper types and produces the associated array of primitives. The first tool has two options, represented by an overloaded static method, array( ). The first version of the method takes an existing array and fills it using a Generator, and the second version takes a Class object, a Generator, and the desired number of elements, and creates a new array, again filling it using the Generator. Notice that this tool only produces arrays of Object subtypes and cannot create primitive arrays:
```java
//: net/mindview/util/Generated.java
package net.mindview.util;
import java.util.*;
public class Generated {
// Fill an existing array:
public static <T> T[] array(T[] a, Generator<T> gen) {
return new CollectionData<T>(gen, a.length).toArray(a);
}
// Create a new array:
@SuppressWarnings("unchecked")
public static <T> T[] array(Class<T> type,
Generator<T> gen, int size) {
T[] a =
(T[])java.lang.reflect.Array.newInstance(type, size);
return new CollectionData<T>(gen, size).toArray(a);
}
} ///:~
```

<!--p574-->
The CollectionData class will be defined in the Containers in Depth chapter. It creates a Collection object filled with elements produced by the Generator gen. The number of elements is determined by the second constructor argument. All Collection subtypes have a toArray( ) method that will fill the argument array with the elements from the Collection. Arrays The second method uses reflection to dynamically create a new array of the appropriate type and size. This is then filled using the same technique as the first method. We can test Generated using one of the CountingGenerator classes defined in the previous section:
```java
//: arrays/TestGenerated.java
import java.util.*;
import net.mindview.util.*;
public class TestGenerated {
public static void main(String[] args) {
Integer[] a = { 9, 8, 7, 6 };
System.out.println(Arrays.toString(a));
a = Generated.array(a,new CountingGenerator.Integer());
System.out.println(Arrays.toString(a));
Integer[] b = Generated.array(Integer.class,
new CountingGenerator.Integer(), 15);
System.out.println(Arrays.toString(b));
}
} /* Output:
[9, 8, 7, 6]
[0, 1, 2, 3]
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
*///:~
```
Even though the array a is initialized, those values are overwritten by passing it through Generated.array( ), which replaces the values (but leaves the original array in place). The initialization of b shows how you can create a filled array from scratch. Generics don’t work with primitives, and we want to use the generators to fill primitive arrays. To solve the problem, we create a converter that takes any array of wrapper objects and converts it to an array of the associated primitive types. Without this tool, we would have to create special case generators for all the primitives.

<!--p575-->
```java
//: net/mindview/util/ConvertTo.java
package net.mindview.util;
public class ConvertTo {
public static boolean[] primitive(Boolean[] in) {
boolean[] result = new boolean[in.length];
for(int i = 0; i < in.length; i++)
result[i] = in[i]; // Autounboxing
return result;
}
public static char[] primitive(Character[] in) {
char[] result = new char[in.length];
for(int i = 0; i < in.length; i++)
result[i] = in[i];
return result;
}
public static byte[] primitive(Byte[] in) {
byte[] result = new byte[in.length];
for(int i = 0; i < in.length; i++)
result[i] = in[i];
return result;
}
public static short[] primitive(Short[] in) {
short[] result = new short[in.length];
for(int i = 0; i < in.length; i++)
result[i] = in[i];
return result;
}
public static int[] primitive(Integer[] in) {
int[] result = new int[in.length];
for(int i = 0; i < in.length; i++)
result[i] = in[i];
return result;
}
public static long[] primitive(Long[] in) {
long[] result = new long[in.length];
for(int i = 0; i < in.length; i++)
result[i] = in[i];
return result;
}
public static float[] primitive(Float[] in) {
float[] result = new float[in.length];
for(int i = 0; i < in.length; i++)
result[i] = in[i];
return result;
}
public static double[] primitive(Double[] in) {
double[] result = new double[in.length];
for(int i = 0; i < in.length; i++)
result[i] = in[i];
return result;
}
} ///:~
```
Each version of primitive( ) creates an appropriate primitive array of the correct length, then copies the elements from the in array of wrapper types. Notice that autounboxing takes place in the expression:
```java
result[i] = in [1];
```
Here’s an example that shows how you can use ConvertTo with both versions of Generated.array( ):
```java
//: arrays/PrimitiveConversionDemonstration.java
import java.util.*;
import net.mindview.util.*;
public class PrimitiveConversionDemonstration {
public static void main(String[] args) {
Integer[] a = Generated.array(Integer.class,
new CountingGenerator.Integer(), 15);
int[] b = ConvertTo.primitive(a);
System.out.println(Arrays.toString(b));
boolean[] c = ConvertTo.primitive(
Generated.array(Boolean.class,
new CountingGenerator.Boolean(), 7));
System.out.println(Arrays.toString(c));
}
} /* Output:
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
[true, false, true, false, true, false, true]
*///:~
```
Finally, here’s a program that tests the array generation tools using RandomGenerator classes:
```java
//: arrays/TestArrayGeneration.java
```

<!--p576-->
Arrays
```java
// Test the tools that use generators to fill arrays.
import java.util.*;
import net.mindview.util.*;
import static net.mindview.util.Print.*;
public class TestArrayGeneration {
public static void main(String[] args) {
int size = 6;
boolean[] a1 = ConvertTo.primitive(Generated.array(
Boolean.class, new RandomGenerator.Boolean(), size));
print("a1 = " + Arrays.toString(a1));
byte[] a2 = ConvertTo.primitive(Generated.array(
Byte.class, new RandomGenerator.Byte(), size));
print("a2 = " + Arrays.toString(a2));
char[] a3 = ConvertTo.primitive(Generated.array(
Character.class,
new RandomGenerator.Character(), size));
print("a3 = " + Arrays.toString(a3));
short[] a4 = ConvertTo.primitive(Generated.array(
Short.class, new RandomGenerator.Short(), size));
print("a4 = " + Arrays.toString(a4));
int[] a5 = ConvertTo.primitive(Generated.array(
Integer.class, new RandomGenerator.Integer(), size));
print("a5 = " + Arrays.toString(a5));
long[] a6 = ConvertTo.primitive(Generated.array(
Long.class, new RandomGenerator.Long(), size));
print("a6 = " + Arrays.toString(a6));
float[] a7 = ConvertTo.primitive(Generated.array(
Float.class, new RandomGenerator.Float(), size));
print("a7 = " + Arrays.toString(a7));
double[] a8 = ConvertTo.primitive(Generated.array(
Double.class, new RandomGenerator.Double(), size));
print("a8 = " + Arrays.toString(a8));
}
} /* Output:
a1 = [true, false, true, false, false, true]
a2 = [104, -79, -76, 126, 33, -64]
a3 = [Z, n, T, c, Q, r]
a4 = [-13408, 22612, 15401, 15161, -28466, -12603]
a5 = [7704, 7383, 7706, 575, 8410, 6342]
a6 = [7674, 8804, 8950, 7826, 4322, 896]
a7 = [0.01, 0.2, 0.4, 0.79, 0.27, 0.45]
a8 = [0.16, 0.87, 0.7, 0.66, 0.87, 0.59]
*///:~
```

<!--p577-->
This also ensures that each version of ConvertTo.primitive( ) works correctly. Exercise 11:(2) Show that autoboxing doesn’t work with arrays. Exercise 12:(1) Create an initialized array of double using CountingGenerator. Print the results. Exercise 13: (2) Fill a String using CountingGenerator.Character. Exercise 14:(6) Create an array of each primitive type, then fill each array by using CountingGenerator. Print each array. Exercise 15:(2) Modify ContainerComparison.java by creating a Generator for BerylliumSphere, and change main( ) to use that Generator with Generated.array(). Exercise 16:(3) Starting with CountingGenerator.java, create a SkipGenerator class that produces new values by incrementing according to a constructor argument. Modify TestArrayGeneration.java to show that your new class works correctly. Exercise 17:(5) Create and test a Generator for BigDecimal, and ensure that it works with the Generated methods.
## Arrays utilities
In java.util, you’ll find the Arrays class, which holds a set of static utility methods for arrays. There are six basic methods: equals( ), to compare two arrays for equality (and a deepEquals( ) for multidimensional arrays); fill( ), which you’ve seen earlier in this chapter; sort( ), to sort an array; binarySearch( ), to find an element in a sorted array; toString( ), to produce a String representation for an array; and hashCode( ), to produce the hash value of an array (you’ll learn what this means in the Containers in Depth chapter). All of these methods are overloaded for all the primitive types and Objects. In addition, Arrays.asList( ) takes any sequence or array and turns it into a List container—this method was covered in the Holding Your Objects chapter. Before discussing the Arrays methods, there’s one other useful method that isn’t part of Arrays. Copying an array The Java standard library provides a static method, System.arraycopy( ), which can copy arrays far more quickly than if you use a for loop to perform the copy by hand. System.arraycopyC ) is overloaded to handle all types. Here’s an example that manipulates arrays of int:
```java
//: arrays/CopyingArrays.java
// Using System.arraycopy()
import java.util.*;
import static net.mindview.util.Print.*;
public class CopyingArrays {
public static void main(String[] args) {
int[] i = new int[7];
int[] j = new int[10];
Arrays.fill(i, 47);
Arrays.fill(j, 99);
print("i = " + Arrays.toString(i));
print("j = " + Arrays.toString(j));
System.arraycopy(i, 0, j, 0, i.length);
print("j = " + Arrays.toString(j));
int[] k = new int[5];
Arrays.fill(k, 103);
System.arraycopy(i, 0, k, 0, k.length);
print("k = " + Arrays.toString(k));
Arrays.fill(k, 103);
System.arraycopy(k, 0, i, 0, k.length);
print("i = " + Arrays.toString(i));
// Objects:
Integer[] u = new Integer[10];
Integer[] v = new Integer[5];
Arrays.fill(u, new Integer(47));
```

<!--p578-->
Arrays
```java
Arrays.fill(v, new Integer(99));
print("u = " + Arrays.toString(u));
print("v = " + Arrays.toString(v));
System.arraycopy(v, 0, u, u.length/2, v.length);
print("u = " + Arrays.toString(u));
}
} /* Output:
i = [47, 47, 47, 47, 47, 47, 47]
j = [99, 99, 99, 99, 99, 99, 99, 99, 99, 99]
j = [47, 47, 47, 47, 47, 47, 47, 99, 99, 99]
k = [47, 47, 47, 47, 47]
i = [103, 103, 103, 103, 103, 47, 47]
u = [47, 47, 47, 47, 47, 47, 47, 47, 47, 47]
v = [99, 99, 99, 99, 99]
u = [47, 47, 47, 47, 47, 99, 99, 99, 99, 99]
*///:~
```
The arguments to arraycopy( ) are the source array, the offset into the source array from whence to start copying, the destination array, the offset into the destination array where the copying begins, and the number of elements to copy. Naturally, any violation of the array boundaries will cause an exception. The example shows that both primitive arrays and object arrays can be copied. However, if you copy arrays of objects, then only the references get copied—there’s no duplication of the objects themselves. This is called a shallow copy (see the online supplements for this book for more details). System.arraycopy( ) will not perform autoboxing or autounboxing—the two arrays must be of exactly the same type. Exercise 18:(3) Create and fill an array of BerylliumSphere. Copy this array to a new array and show that it’s a shallow copy. Comparing arrays Arrays provides the equals( ) method to compare entire arrays for equality, which is overloaded for all the primitives and for Object. To be equal, the arrays must have the same number of elements, and each element must be equivalent to each corresponding element in the other array, using the equals( ) for each element. (For primitives, that primitive’s wrapper class equals( ) is used; for example, Integer.equals( ) for int.) For example:

<!--p579-->
```java
//: arrays/ComparingArrays.java
// Using Arrays.equals()
import java.util.*;
import static net.mindview.util.Print.*;
public class ComparingArrays {
public static void main(String[] args) {
int[] a1 = new int[10];
int[] a2 = new int[10];
Arrays.fill(a1, 47);
Arrays.fill(a2, 47);
print(Arrays.equals(a1, a2));
a2[3] = 11;
print(Arrays.equals(a1, a2));
String[] s1 = new String[4];
Arrays.fill(s1, "Hi");
```
Arrays
```java
String[] s2 = { new String("Hi"), new String("Hi"),
new String("Hi"), new String("Hi") };
print(Arrays.equals(s1, s2));
}
} /* Output:
true
false
true
*///:~
```
Originally, a1 and a2 are exactly equal, so the output is "true," but then one of the elements is changed, which makes the result "false." In the last case, all the elements of s1 point to the same object, but s2 has five unique objects. However, array equality is based on contents (via Object.equals( )), so the result is "true." Exercise 19:(2) Create a class with an int field that’s initialized from a constructor argument. Create two arrays of these objects, using identical initialization values for each array, and show that Arrays.equals( ) says that they are unequal. Add an equals( ) method to your class to fix the problem. Exercise 20:(4) Demonstrate deepEquals( ) for multidimensional arrays. Array element comparisons Sorting must perform comparisons based on the actual type of the object. Of course, one approach is to write a different sorting method for every different type, but such code is not reusable for new types. A primary goal of programming design is to "separate things that change from things that stay the same," and here, the code that stays the same is the general sort algorithm, but the thing that changes from one use to the next is the way objects are compared. So instead of placing the comparison code into many different sort routines, the Strategy design pattern is used.2With a Strategy, the part of the code that varies is encapsulated inside a separate class (the Strategy object). You hand a Strategy object to the code that’s always the same, which uses the Strategy to fulfill its algorithm. That way, you can make different objects to express different ways of comparison and feed them to the same sorting code. Java has two ways to provide comparison functionality. The first is with the "natural" comparison method that is imparted to a class by implementing the java.lang.Comparable interface. This is a very simple interface with a single method, compareTo( ). This method takes another object of the same type as an argument and produces a negative value if the current object is less than the argument, zero if the argument is equal, and a positive value if the current object is greater than the argument. Here’s a class that implements Comparable and demonstrates the comparability by using the Java standard library method Arrays.sort( ):
```java
//: arrays/CompType.java
// Implementing Comparable in a class.
import java.util.*;
import net.mindview.util.*;
import static net.mindview.util.Print.*;
```

<!--p580-->
2Design Patterns, Erich Gamma et al. (Addison-Wesley, 1995). See Thinking in Patterns (with Java) at www.MindView.net.
```java
public class CompType implements Comparable<CompType> {
int i;
int j;
private static int count = 1;
public CompType(int n1, int n2) {
i = n1;
j = n2;
}
public String toString() {
String result = "[i = " + i + ", j = " + j + "]";
if(count++ % 3 == 0)
result += "\n";
return result;
}
public int compareTo(CompType rv) {
return (i < rv.i ? -1 : (i == rv.i ? 0 : 1));
}
private static Random r = new Random(47);
public static Generator<CompType> generator() {
return new Generator<CompType>() {
public CompType next() {
return new CompType(r.nextInt(100),r.nextInt(100));
}
};
}
public static void main(String[] args) {
CompType[] a =
Generated.array(new CompType[12], generator());
print("before sorting:");
print(Arrays.toString(a));
Arrays.sort(a);
print("after sorting:");
print(Arrays.toString(a));
}
} /* Output:
before sorting:
[[i = 58, j = 55], [i = 93, j = 61], [i = 61, j = 29]
, [i = 68, j = 0], [i = 22, j = 7], [i = 88, j = 28]
, [i = 51, j = 89], [i = 9, j = 78], [i = 98, j = 61]
, [i = 20, j = 58], [i = 16, j = 40], [i = 11, j = 22]
]
after sorting:
[[i = 9, j = 78], [i = 11, j = 22], [i = 16, j = 40]
, [i = 20, j = 58], [i = 22, j = 7], [i = 51, j = 89]
, [i = 58, j = 55], [i = 61, j = 29], [i = 68, j = 0]
, [i = 88, j = 28], [i = 93, j = 61], [i = 98, j = 61]
]
*///:~
```

<!--p581-->
When you define the comparison method, you are responsible for deciding what it means to compare one of your objects to another. Here, only the i values are used in the comparison, and the j values are ignored. The generator( ) method produces an object that implements the Generator interface by creating an anonymous inner class. This builds CompType objects by initializing them with random values. In main( ), the generator is used to fill an array of CompType, which is then sorted. If Comparable hadn’t been implemented, then you’d get a ClassCastException at run time when you tried to call sort( ). This is because sort( ) casts its argument to Comparable. Now suppose someone hands you a class that doesn’t implement Comparable, or hands you this class that does implement Comparable, but you decide you don’t like the way it works and would rather have a different comparison method for the type. To solve the problem, you create a separate class that implements an interface called Comparator (briefly introduced in the Holding Your Objects chapter). This is an example of the Strategy design pattern. It has two methods, compare( ) and equals( ). However, you don’t have to implement equals( ) except for special performance needs, because anytime you create a class, it is implicitly inherited from Object, which has an equals( ). So you can just use the default Object equals( ) and satisfy the contract imposed by the interface. The Collections class (which we’ll look at more in the next chapter) contains a method reverseOrder( ) that produces a Comparator to reverse the natural sorting order. This can be applied to CompType:
```java
//: arrays/Reverse.java
// The Collections.reverseOrder() Comparator
import java.util.*;
import net.mindview.util.*;
import static net.mindview.util.Print.*;
public class Reverse {
public static void main(String[] args) {
CompType[] a = Generated.array(
new CompType[12], CompType.generator());
print("before sorting:");
print(Arrays.toString(a));
Arrays.sort(a, Collections.reverseOrder());
print("after sorting:");
print(Arrays.toString(a));
}
} /* Output:
before sorting:
[[i = 58, j = 55], [i = 93, j = 61], [i = 61, j = 29]
, [i = 68, j = 0], [i = 22, j = 7], [i = 88, j = 28]
, [i = 51, j = 89], [i = 9, j = 78], [i = 98, j = 61]
, [i = 20, j = 58], [i = 16, j = 40], [i = 11, j = 22]
]
after sorting:
[[i = 98, j = 61], [i = 93, j = 61], [i = 88, j = 28]
, [i = 68, j = 0], [i = 61, j = 29], [i = 58, j = 55]
, [i = 51, j = 89], [i = 22, j = 7], [i = 20, j = 58]
, [i = 16, j = 40], [i = 11, j = 22], [i = 9, j = 78]
]
*///:~
```
You can also write your own Comparator. This one compares CompType objects based on their j values rather than their i values:
```java
//: arrays/ComparatorTest.java
// Implementing a Comparator for a class.
import java.util.*;
import net.mindview.util.*;
import static net.mindview.util.Print.*;
class CompTypeComparator implements Comparator<CompType> {
public int compare(CompType o1, CompType o2) {
return (o1.j < o2.j ? -1 : (o1.j == o2.j ? 0 : 1));
}
}
public class ComparatorTest {
```

<!--p582-->
Arrays
```java
public static void main(String[] args) {
CompType[] a = Generated.array(
new CompType[12], CompType.generator());
print("before sorting:");
print(Arrays.toString(a));
Arrays.sort(a, new CompTypeComparator());
print("after sorting:");
print(Arrays.toString(a));
}
} /* Output:
before sorting:
[[i = 58, j = 55], [i = 93, j = 61], [i = 61, j = 29]
, [i = 68, j = 0], [i = 22, j = 7], [i = 88, j = 28]
, [i = 51, j = 89], [i = 9, j = 78], [i = 98, j = 61]
, [i = 20, j = 58], [i = 16, j = 40], [i = 11, j = 22]
]
after sorting:
[[i = 68, j = 0], [i = 22, j = 7], [i = 11, j = 22]
, [i = 88, j = 28], [i = 61, j = 29], [i = 16, j = 40]
, [i = 58, j = 55], [i = 20, j = 58], [i = 93, j = 61]
, [i = 98, j = 61], [i = 9, j = 78], [i = 51, j = 89]
]
*///:~
```
Exercise 21:(3) Try to sort an array of the objects in Exercise 18. Implement Comparable to fix the problem. Now create a Comparator to sort the objects into reverse order. Sorting an array With the built-in sorting methods, you can sort any array of primitives, or any array of objects that either implements Comparable or has an associated Comparator.3Here’s an example that generates random String objects and sorts them:
```java
//: arrays/StringSorting.java
// Sorting an array of Strings.
import java.util.*;
import net.mindview.util.*;
import static net.mindview.util.Print.*;
public class StringSorting {
public static void main(String[] args) {
String[] sa = Generated.array(new String[20],
new RandomGenerator.String(5));
print("Before sort: " + Arrays.toString(sa));
Arrays.sort(sa);
print("After sort: " + Arrays.toString(sa));
Arrays.sort(sa, Collections.reverseOrder());
print("Reverse sort: " + Arrays.toString(sa));
Arrays.sort(sa, String.CASE_INSENSITIVE_ORDER);
print("Case-insensitive sort: " + Arrays.toString(sa));
}
} /* Output:
Before sort: [YNzbr, nyGcF, OWZnT, cQrGs, eGZMm, JMRoE, suEcU, OneOE,
dLsmw, HLGEa, hKcxr, EqUCB, bkIna, Mesbt, WHkjU, rUkZP, gwsqP, zDyCy,
RFJQA, HxxHv]
```

<!--p583-->
3 Surprisingly, there was no support in Java 1.0 or 1.1 for sorting Strings.
```java
After sort: [EqUCB, HLGEa, HxxHv, JMRoE, Mesbt, OWZnT, OneOE, RFJQA,
WHkjU, YNzbr, bkIna, cQrGs, dLsmw, eGZMm, gwsqP, hKcxr, nyGcF, rUkZP,
suEcU, zDyCy]
Reverse sort: [zDyCy, suEcU, rUkZP, nyGcF, hKcxr, gwsqP, eGZMm, dLsmw,
cQrGs, bkIna, YNzbr, WHkjU, RFJQA, OneOE, OWZnT, Mesbt, JMRoE, HxxHv,
HLGEa, EqUCB]
Case-insensitive sort: [bkIna, cQrGs, dLsmw, eGZMm, EqUCB, gwsqP, hKcxr,
HLGEa, HxxHv, JMRoE, Mesbt, nyGcF, OneOE, OWZnT, RFJQA, rUkZP, suEcU,
WHkjU, YNzbr, zDyCy]
*///:~
```
One thing you’ll notice about the output in the String sorting algorithm is that it’s lexicographic, so it puts all the words starting with uppercase letters first, followed by all the words starting with lowercase letters. (Telephone books are typically sorted this way.) If you want to group the words together regardless of case, use String.CASE_INSENSITIVE_ORDER as shown in the last call to sort( ) in the above example. The sorting algorithm that’s used in the Java standard library is designed to be optimal for the particular type you’re sorting—a Quicksort for primitives, and a stable merge sort for objects. You don’t need to worry about performance unless your profiler points you to the sorting process as a bottleneck. Searching a sorted array Once an array is sorted, you can perform a fast search for a particular item by using Arrays.binarySearch( ). However, if you try to use binarySearchC ) on an unsorted array the results will be unpredictable. The following example uses a RandomGenerator.Integer to fill an array, and then uses the same generator to produce search values:
```java
//: arrays/ArraySearching.java
// Using Arrays.binarySearch().
import java.util.*;
import net.mindview.util.*;
import static net.mindview.util.Print.*;
public class ArraySearching {
public static void main(String[] args) {
Generator<Integer> gen =
new RandomGenerator.Integer(1000);
int[] a = ConvertTo.primitive(
Generated.array(new Integer[25], gen));
Arrays.sort(a);
print("Sorted array: " + Arrays.toString(a));
while(true) {
int r = gen.next();
int location = Arrays.binarySearch(a, r);
if(location >= 0) {
print("Location of " + r + " is " + location +
", a[" + location + "] = " + a[location]);
break; // Out of while loop
}
}
}
} /* Output:
Sorted array: [128, 140, 200, 207, 258, 258, 278, 288, 322, 429, 511,
520, 522, 551, 555, 589, 693, 704, 809, 861, 861, 868, 916, 961, 998]
```

<!--p584-->
Arrays
```java
Location of 322 is 8, a[8] = 322
*///:~
```
In the while loop, random values are generated as search items until one of them is found. Arrays.binarySearch( ) produces a value greater than or equal to zero if the search item is found. Otherwise, it produces a negative value representing the place that the element should be inserted if you are maintaining the sorted array by hand. The value produced is
```java
-(insertion point) - 1
```
The insertion point is the index of the first element greater than the key, or a.size( ), if all elements in the array are less than the specified key. If an array contains duplicate elements, there is no guarantee which of those duplicates will be found. The search algorithm is not designed to support duplicate elements, but rather to tolerate them. If you need a sorted list of non-duplicated elements, use a TreeSet (to maintain sorted order) or LinkedHashSet (to maintain insertion order). These classes take care of all the details for you automatically. Only in cases of performance bottlenecks should you replace one of these classes with a hand-maintained array. If you sort an object array using a Comparator (primitive arrays do not allow sorting with a Comparator), you must include that same Comparator when you perform a binarySearch( ) (using the overloaded version of binarySearch( )). For example, the StringSorting.java program can be modified to perform a search:
```java
//: arrays/AlphabeticSearch.java
// Searching with a Comparator.
import java.util.*;
import net.mindview.util.*;
public class AlphabeticSearch {
public static void main(String[] args) {
String[] sa = Generated.array(new String[30],
new RandomGenerator.String(5));
Arrays.sort(sa, String.CASE_INSENSITIVE_ORDER);
System.out.println(Arrays.toString(sa));
int index = Arrays.binarySearch(sa, sa[10],
String.CASE_INSENSITIVE_ORDER);
System.out.println("Index: "+ index + "\n"+ sa[index]);
}
} /* Output:
[bkIna, cQrGs, cXZJo, dLsmw, eGZMm, EqUCB, gwsqP, hKcxr, HLGEa, HqXum,
HxxHv, JMRoE, JmzMs, Mesbt, MNvqe, nyGcF, ogoYW, OneOE, OWZnT, RFJQA,
rUkZP, sgqia, slJrL, suEcU, uTpnX, vpfFv, WHkjU, xxEAJ, YNzbr, zDyCy]
Index: 10
HxxHv
*///:~
```

<!--p585-->

<!--p586-->
The Comparator must be passed to the overloaded binarySearch( ) as the third argument. In this example, success is guaranteed because the search item is selected from the array itself. Exercise 22:(2) Show that the results of performing a binarySearch( ) on an unsorted array are unpredictable. Exercise 23:(2) Create an array of Integer, fill it with random int values (using autoboxing), and sort it into reverse order using a Comparator. Exercise 24:(3) Show that the class from Exercise 19 can be searched. Arrays Summary In this chapter, you’ve seen that Java provides reasonable support for fixedsized, low-level arrays. This sort of array emphasizes performance over flexibility, just like the C and C++ array model. In the initial version of Java, fixed-sized, low-level arrays were absolutely necessary, not only because the Java designers chose to include primitive types (also for performance), but because the support for containers in that version was very minimal. Thus, in early versions of Java, it was always reasonable to choose arrays. In subsequent versions of Java, container support improved significantly, and now containers tend to outshine arrays in all ways except for performance, and even then, the performance of containers has been significantly improved. As stated in other places in this book, performance problems are usually never where you imagine them to be, anyway. With the addition of autoboxing and generics, holding primitives in containers has become effortless, which further encourages you to replace low-level arrays with containers. Because generics produce type-safe containers, arrays no long have an advantage on that front, either. As noted in this chapter and as you’ll see when you try to use them, generics are fairly hostile towards arrays. Often, even when you can get generics and arrays to work together in some form (as you’ll see in the next chapter), you’ll still end up with "unchecked" warnings during compilation. On several occasions I have been told directly by Java language designers that I should be using containers instead of arrays, when we were discussing particular examples (I was using arrays to demonstrate specific techniques and so I did not have that option). All of these issues indicate that you should "prefer containers to arrays" when programming in recent versions of Java. Only when it’s proven that performance is an issue (and that switching to an array will make a difference) should you refactor to arrays. This is a rather bold statement, but some languages have no fixed-sized, lowlevel arrays at all. They only have resizable containers with significantly more functionality than C/C++/Java- style arrays. Python,4 for example, has a list type that uses basic array syntax, but has much greater functionality—you can even inherit from it:
```java
#: arrays/PythonLists.py
aList = [1, 2, 3, 4, 5]
print type(aList) # <type ‘list’>
print aList # [1, 2, 3, 4, 5]
print aList[4] # 5 Basic list indexing
aList.append(6) # lists can be resized
aList += [7, 8] # Add a list to a list
print aList # [1, 2, 3, 4, 5, 6, 7, 8]
aSlice = aList[2:4]
print aSlice # [3, 4]
class MyList(list): # Inherit from list
# Define a method, ‘this’ pointer is explicit:
def getReversed(self):
reversed = self[:] # Copy list using slices
reversed.reverse() # Built-in list method
return reversed
```

<!--p587-->
4 See www.Python.org. Arrays
```java
list2 = MyList(aList) # No ‘new’ needed for object creation
print type(list2) # <class ‘__main__.MyList’>
print list2.getReversed() # [8, 7, 6, 5, 4, 3, 2, 1]
#:~
```
Basic Python syntax was introduced in the previous chapter. Here, a list is created by simply surrounding a comma-separated sequence of objects with square brackets. The result is an object with a runtime type of list (the output of the print statements is shown as comments on the same line). The result of printing a list is the same as that of using Arrays.toString() in Java. Creating a sub-sequence of a list is accomplished with "slicing," by placing the’:’ operator inside the index operation. The list type has many more builtin operations. MyList is a class definition; the base classes are placed within the parentheses. Inside the class, def statements produce methods, and the first argument to the method is automatically the equivalent of this in Java, except that in Python it’s explicit and the identifier self is used by convention (it’s not a keyword). Notice how the constructor is automatically inherited. Although everything in Python really is an object (including integral and floating point types), you still have an escape hatch in that you can optimize performance-critical portions of your code by writing extensions in C, C++ or a special tool called Pyrex, which is designed to easily speed up your code. This way you can have object purity without being prevented from performance improvements. The PHP language5 goes even further by having only a single array type, which acts as both an int-indexed array and an associative array (a Map). It’s interesting to speculate, after this many years of Java evolution, whether the designers would put primitives and low-level arrays in the language if they were to start over again. If these were left out, it would be possible to make a truly pure object-oriented language (despite claims, Java is not a pure 0 0 language, precisely because of the low-level detritus). The initial argument for efficiency always seems compelling, but over time we have seen an evolution away from this idea and towards the use of higher-level components like containers. Add to this the fact that if containers can be built into the core language as they are in some languages, then the compiler has a much better opportunity to optimize. Green-fields speculation aside, we are certainly stuck with arrays, and you will see them when reading code. Containers, however, are almost always a better choice. Exercise 25: (3) Rewrite PythonLists.py in Java. Solutions to selected exercises can be found in the electronic document The Thinking in Java Annotated Solution Guide, available for sale from www.MindView.net. 5 See www.php.net.