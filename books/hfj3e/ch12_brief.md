# Chapter 12: Chapter 12: Lambdas and Streams: What, Not How

pages 407-458

while this is true do this thing; for all these items if it looks like this then do this; and so on. We’ve also seen that we don’t have to do everything ourselves. The JDK contains library code, like the Collections API we saw in the previous chapter, that we can use instead of writing everything from scratch. This library code isn’t just limited to collections to put data into; there are methods that will do common tasks for us, so we just need to tell them what we want and

```java
List<String> allColors = List.of("Red", "Blue", "Yellow");
allColors.forEach(color -> System.out.println(color));
```

In this chapter we'll look at the Streams API. You’ll see how helpful lambda expressions can be when you're using streams, and you'll learn how to use the Streams API to query and transform the data in a collection.

## Tell the computer WHAT you want

```java
List<String> allColors = List.of("Red", "Blue", "Yellow");
for (String color : allColors) {
System.out.println(color);
}
```

```java
Red
Blue
Yellow
```

## When for loops go wrong

```java
class MixForLoops {
public static void main(String [] args) {
List<Integer> nums = List.of(1, 2, 3, 4, 5);
String output = "";
System.out.println(output);
}
}
```

```java
for (int i = 1; i < nums.size(); i++)
output += nums.get(i) + " ";
```

```java
for (int i = 0; i <= nums.size(); i++)
output += nums.get(i) + " ";
for (int i = 0; i <= nums.length; i++)
output += nums.get(i) + " ";
for (Integer num : nums)
output += nums + " ";
Compiler error
2 3 4 5
Exception thrown
[1, 2, 3, 4, 5]
[1, 2, 3, 4, 5]
[1, 2, 3, 4, 5]
[1, 2, 3, 4, 5]
[1, 2, 3, 4, 5]
1 2 3 4 5
```

## Small errors in common code can be hard to spot

like they would print out all the values in the List in order. Compiler errors can be easiest to spot, because your IDE or compiler will tell you the code is wrong, and Exceptions (which we’ll see in Chapter 13, Risky Behavior) can also point to a problem in the code. But it can be trickier to spot code that produces incorrect output just by looking at the code. Using a method like forEach takes care of the “boilerplate,” the repetitive and common code like the for loop. Using forEach, passing in only the thing we want to do, can reduce accidental errors in our code.

## Building blocks of common operations

The ways we search our collections, and the types of information we want to output from those collections, can be quite similar even on different types of collections containing different types of Objects. Imagine what you might want do to with a Collection: “give me just the items that meet some crite­ ria,” “change all the items using these steps,” “remove all duplicates,” and the example we worked through in the previous chapter: “sort the elements in this way.”

It’s not too hard to go one step further and assume each of these collection operations could be given a name that tells us what will happen to our collection. Changes the current element in the stream into something else filter We know this is all new, but have a go at matching each operation name to the description of what it does. Try not to look at the next page as you complete it, as that will give the game away!

## Introducing the Streams API

## Getting started with Streams

```java
List<String> strings = List.of("I", "am", "a", "list", "of", "Strings");
Stream<String> stream = strings.stream();
```

```java
System.out.println("limit = " + limit);
```

```java
limit = java.util.stream.SliceOps$1@7a0ac6e3
```

## Getting a result from a Stream

```java
List<String> strings = List.of("I", "am", "a", "list", "of", "Strings");
Stream<String> stream = strings.stream();
Stream<String> limit = stream.limit(4);
long result = limit.count();
System.out.println("result = " + result);
```

```java
result = 4
```

Yes, we’ve thrown a lot of new words at you: streams; intermediate operations; terminal operations... And we still haven’t told you what streams can do! To start to get a feel for what we can do with streams, we going to show code for a simple use of the Streams API. After that, we’ll step back and learn more about what we’re seeing here. File Edit Window Help WellDuh %java LimitWithStream Call the count terminal operator, and store the output in a variable called result

```java
List<String> result = limit.collect(Collectors.toList());
System.out.println("result = " + result);
```

```java
result = [I, am, a, list]
```

might seem intimidating with all the generic types, but the simplest case is straightforward: File Edit Window Help FinallyAResult %java LimitWithStream Finally, we have a result that looks like something we would have expected: we had a List of Strings, and we asked to limit that list to the first four items and then collect those four items into a new List. Terminal operation that will collect the output into some sort of Object.

## Stream operations are building blocks

```java
.stream()
```

```java
List<String> strings = List.of("I", "am", "a", "list", "of", "Strings");
List<String> result = strings.stream()
.limit(4)
.collect(Collectors.toList());
System.out.println("result = " + result);
```

## Building blocks can be stacked and combined

```java
List<String> strings = List.of("I", "am", "a", "list", "of", "Strings");
List<String> result = strings.stream()
.sorted()
.limit(4)
.collect(Collectors.toList());
System.out.println("result = " + result);
```

```java
result = [I, Strings, a, am]
```

## Customizing the building blocks

If we didn’t want to use the natural ordering to sort our Strings, we could define a specific way to sort them. It’s possible to set the sort criteria for the sorted method (remember, we did something similar in the previous chapter when we sorted Lou’s song list). This method from the String class compares the String with another String, in a way that ignores upper or lowercase. Lambda expression that tells the sorted method how to sort the strings in the stream. This lambda expression represents a Comparator, which we talked about in the previous chapter. We'll recap lambdas later in this chapter.

```java
result = [a, am, I, list]
List<String> result = strings.stream()
.sorted((s1, s2) -> s1.compareToIgnoreCase(s2))
.limit(4)
.collect(Collectors.toList());
```

## Create complex pipelines block by block

```java
List<String> result = strings.stream()
.sorted((s1, s2) -> s1.compareToIgnoreCase(s2))
.skip(2)
.limit(4)
.collect(Collectors.toList());
```

```java
result = [I, list, of, Strings]
```

## Yes, because Streams are lazy

## Collecting to a List

```java
List<String> result = strings.stream()
.sorted()
.skip(2)
.limit(4)
.collect(Collectors.toList());
```

## Terminal operations do all the work

Since intermediate operations are lazy, it’s up to the terminal operation to do everything. Perform all the intermediate operations as efficiently as possible. Ideally, just going through the original data once. Work out the result of the operation, which is defined by the terminal operation itself. For example, this could be a list of values, a single value, or a boolean (true/false). Return the result.

## Guidelines for working with streams

It might seem useful to store a Stream representing a query, and reuse it in multiple places, either because the query itself is useful or because you want to build on it and add to it. But once a terminal operation has been called on a stream, you can’t reuse any parts of that stream; you have to create a new one. Once a pipeline has executed, that stream is closed and can’t be used in another pipeline, even if you stored part of it in a variable for reusing elsewhere. If you try to reuse a stream in any way, you’ll get an Exception.

```java
Stream<String> limit = strings.stream()
.limit(4);
List<String> result = limit.collect(Collectors.toList());
List<String> result2 = limit.collect(Collectors.toList());
```

```java
Exception in thread "main" java.lang.IllegalStateException: stream has
already been operated upon or closed
at java.base/java.util.stream.AbstractPipeline.
evaluate(AbstractPipeline.java:229)
```

```java
List<String> strings = List.of("I", "am", "a", "list", "of", "Strings");
Stream<String> limit = strings.stream()
.limit(4)
.collect(Collectors.toList());
System.out.println("strings = " + strings);
System.out.println("result = " + result);
```

```java
strings = [I, am, a, list, of, Strings]
result = [I, am, a, list]
```

```java
import java.util.*;
.filter(s -> s.endsWith("o"))
List<String> coffeesEndingInO = coffees.stream()
System.out.println(coffeesEndingInO);
.sorted()
.distinct()
List<String> coffees = List.of("Cappuccino",
"Americano", "Espresso","Cortado", "Mocha",
"Cappuccino", "Flat White", "Latte");
.collect(Collectors.toList());
public class CoffeeOrder {
public static void main(String[] args) {
import java.util.stream.*;
}
}
```

```java
[Americano, Cappuccino, Cortado, Espresso]
```

## Hello Lambda, my (not so) old friend

```java
void forEach( ????? ) {
for (Element element : list) {
}
}
```

```java
forEach( item -> System.out.println(item) );
```

## Passing behavior around

```java
void forEach( SomeFunctionalInterface lambda ) {
for (Element element : list) {
lambda.singleAbstractMethodName(element);
}
}
```

## The shape of lambda expressions

```java
public interface Comparator<T> {
int compare(T o1, T o2);
}
(s1, s2) -> s1.compareToIgnoreCase(s2)
```

```java
(String s1, String s2) -> {
return s1.compareToIgnoreCase(s2);
}
```

## Anatomy of a lambda expression

## Variety is the spice of life

```java
(str1, str2) -> {
int l1 = str1.length();
int l2 = str2.length();
return l2 - l1;
}
```

```java
(str1, str2) -> str2.length() - str1.length()
```

If your lambda expression is a single line, it makes it much easier for the compiler to guess what’s going on. Therefore, we can leave out a lot of the “boilerplate” syntax. If we shrink the lambda expression from the last example into a single line, it looks like this: No need for curly braces No need for “return” No semicolons This is the same Functional Interface (Comparator) and performs the same operation. Whether you use multiline lambdas or single-line lambdas is completely up to you. It will

```java
str -> {
String output = "str = " + str;
System.out.println(output);
}
```

```java
@FunctionalInterface
public interface
Consumer<T> {
void accept(T t);
}
```

The Functional Interface’s method might be declared void; i.e., it doesn’t return anything. In these cases, the code inside the lambda is simply run, and you don’t need to return any values from the lambda body. This is the case for lambda expressions in a forEach method. Multiline lambda No return value Look! No round brackets! We’ll see this again in a minute. Method is void on the Functional Interface

The number of parameters the lambda expression needs is dependent upon the number of parameters the Functional Interface’s method takes. The parameter types (e.g., the name “String”) are not usually required, but you can add them if you think it makes it easier to understand the code. You may need to add the types if the compiler can’t automatically work out which Functional Interface your lambda implements.

```java
str -> System.out.println(str)
@FunctionalInterface
public interface Consumer<T> {
void accept(T t);
}
() -> System.out.println("Hello!")
```

```java
@FunctionalInterface
public interface Runnable {
void run();
}
```

```java
(str1, str2) -> str1.compareToIgnoreCase(str2)
@FunctionalInterface
public interface Comparator<T> {
int compare(T o1, T o2);
}
```

## How can I tell if a method takes a lambda?

```java
Comparator<String> comparator = (s1, s2) -> s1.compareToIgnoreCase(s2);
Runnable runnable = () -> System.out.println("Hello!");
Consumer<String> consumer = str -> System.out.println(str);
```

```java
@FunctionalInterface
public interface Predicate<T>
```

we have been doing so far, assign it to a variable. You’ll see it can be treated just like any other Object in Java, because everything in Java is an Object. The variable’s type is the Functional Interface. How does this help us see if a method takes a lambda expression? Well, the method’s parameter type will be a Functional Interface. Take a look at some examples from the Streams API: Stream<T> filter​(Predicate<? super T> predicate)

```java
@FunctionalInterface
public interface Function<T,​R>
@FunctionalInterface
public interface Consumer<T>
```

```java
public interface Consumer<T> {
void accept(T t);
}
public interface Runnable {
void run();
}
public interface Supplier<T> {
T get();
}
public interface Function<T, R> {
R apply(T t);
}
```

## Spotting Functional Interfaces

So far we’ve seen Functional Interfaces that are marked with a @FunctionalInterfaceannotation (we’ll cover annotations in Appendix B), which conveniently tells us this interface has a Single Abstract Method and can be implemented with a lambda expression. Not all functional interfaces are tagged this way, particularly in older code, so it’s useful to understand how to spot a functional interface for yourself.

that need to be overridden by any class that implements this interface. But as of Java 8, interfaces can also contain default and static methods. You saw static methods in Chapter 10, Numbers Matter, and you’ll see them later in this chapter too. These are methods that don’t need to belong to an instance, and are often used as helper methods. Default methods are slightly different. Remember abstract classes from Chapter 8, Serious Poly­ morphism? They had abstract methods that need to be overridden, and standard methods with a body. On an interface, a default method works a bit like a standard method in an abstract class—they have a body, and will be inherited by subclasses.

Both default and static methods have a method body, with defined behavior. With interfaces, any method that is not defined as default or static is an abstract method that must be overridden. How hard can it be? I just have to look for interfaces with only one method! lambdas andstreams

## Functional interfaces in the wild

Now that we know interfaces can have non-abstract methods, we can see there’s a bit more of a trick to identifying interfaces with just one abstract method. Take a look at our old friend, Comparator. It has a lot of methods! And yet it’s still a SAM-type; it has only one Single Abstract Method. It’s a Functional Interface we can implement as a lambda expression. Here it is! This is our Single Abstract Method.

```java
BiPredicate
ActionListener
Function
Iterator
SocketOption
```

## Lou’s back!

The code on the next page is your mock code; calling Songs.getSongs() will give you a List of Song objects that you can assume looks just like the real data from Lou’s jukebox. Type in the Ready-Bake Code on the next page, including filling out the rest of the Song class. When you’ve done that, create a main method that prints out all the songs. What do you expect the output to look like? But now that we know about the Streams API, we know there’s an easier way....

```java
class Songs {
public List<Song> getSongs() {
return List.of(
new Song("$10", "Hitchhiker", "Electronic", 2016, 183),
new Song("Havana", "Camila Cabello", "R&B", 2017, 324),
new Song("Cassidy", "Grateful Dead", "Rock", 1972, 123),
new Song("50 ways", "Paul Simon", "Soft Rock", 1975, 199),
new Song("Hurt", "Nine Inch Nails", "Industrial Rock", 1995, 257),
new Song("Silence", "Delerium", "Electronic", 1999, 134),
new Song("Hurt", "Johnny Cash", "Soft Rock", 2002, 392),
new Song("Watercolour", "Pendulum", "Electronic", 2010, 155),
new Song("The Outsider", "A Perfect Circle", "Alternative Rock", 2004, 312),
new Song("With a Little Help from My Friends", "The Beatles", "Rock", 1967, 168),
new Song("Come Together", "The Beatles", "Blues rock", 1968, 173),
new Song("Come Together", "Ike & Tina Turner", "Rock", 1970, 165),
new Song("With a Little Help from My Friends", "Joe Cocker", "Rock", 1968, 46),
new Song("Immigrant Song", "Karen O", "Industrial Rock", 2011, 12),
new Song("Breathe", "The Prodigy", "Electronic", 1996, 337),
new Song("What's Going On", "Gaye", "R&B", 1971, 420),
new Song("Hallucinate", "Dua Lipa", "Pop", 2020, 75),
new Song("Walk Me Home", "P!nk", "Pop", 2019, 459),
new Song("I am not a woman, I'm a god", "Halsey", "Alternative Rock", 2021, 384),
new Song("Pasos de cero", "Pablo Alborán", "Latin", 2014, 117),
new Song("Smooth", "Santana", "Latin", 1999, 244),
new Song("Immigrant song", "Led Zeppelin", "Rock", 1970, 484));
}
}
public class Song {
private final String title;
private final String artist;
private final String genre;
private final int year;
private final int timesPlayed;
// Practice for you! Create a constructor, all the getters and a toString()
}
```

```java
.stream()
```

diner’s clientele seem to prefer variations on rock music, and he wants to see a list of all the songs that fall under some genre of “rock.” This is the Streams chapter, so clearly the solution is going to involve the Streams API. Remember, there are three types of pieces we can put together to form a solution. output collection Lou said he wants a List of all the Songs that match what he wants, so it sounds like we should use the magic incantation to collect the results to a List.

## Filter a stream to keep certain elements

```java
.stream()
.collect(toList)
.filter( )
```

## Let’s Rock!

```java
@FunctionalInterface
public interface Predicate<T> {
boolean test(T t);
}
```

continues with just the elements that meet our criteria. It should come as no surprise to find that you can use a lambda expression to state which elements we want to keep in the stream. The filter method takes a Predicate. Returns a boolean Has a single parameter Given what we know about the shapes of lambda expressions, we should be able to work out how to write a lambda expression that implements Predicate.

```java
Predicate predicate = ->
```

```java
public class JukeboxStreams {
public static void main(String[] args) {
List<Song> songs = new Songs().getSongs();
List<Song> rockSongs = songs.stream()
.filter(song -> song.getGenre().equals("Rock"))
.collect(Collectors.toList());
System.out.println(rockSongs);
}
}
class Songs {
// as Ready-Bake Code
}
class Song {
// as Ready-Bake Code
}
```

We’ll know what the type of the single parameter is when we plug it into the Stream opera­ tion, since the input type to the lambda will be determined by the types in the stream. The stream pipeline will return a List of Songs. This is a Song because filter() is acting on a Stream of Songs. Puts the results into a List. Get the genre (a String) from the song and see if it’s “Rock.” This will return a true or false.

```java
[Cassidy, Grateful Dead, Rock
With a Little Help from My Friends, The Beatles, Rock,
Come Together, Ike & Tina Turner, Rock,
With a Little Help from My Friends, Joe Cocker, Rock,
Immigrant song, Led Zeppelin, Rock]
```

```java
List<Song> rockSongs = songs.stream()
.filter(song -> song.getGenre().contains("Rock"))
.collect(Collectors.toList());
```

```java
[Cassidy, Grateful Dead, Rock
50 ways, Paul Simon, Soft Rock
Hurt, Nine Inch Nails, Industrial Rock
Hurt, Johnny Cash, Soft Rock
...
```

## Getting clever with filters

sophisticated logic to filter elements in, or out, of the stream. Let’s take our filter one step further and actually do what Lou asked: He wants to see a list of all the songs that fall under some genre of “rock.” He doesn’t want to see just the songs that are classed as “Rock,” but any genre that is kinda Rock-like. We should search for any genre that has the word “Rock” in it somewhere. There’s a method in String that can help us with this, it’s called contains.

## Lou’s Challenge #2: List all the genres

```java
.stream()
.collect(toList)
.map( )
```

```java
List<String> genres = songs.stream()
.map(song -> song.getGenre())
.collect(toList());
```

## Mapping from one type to another

```java
@FunctionalInterface
public interface Function<T, R> {
R apply(T t);
}
```

makes it a little tricky to understand, but Functions do one thing: they take something of one type and return something of a different type. Exactly what’s needed for mapping varies from one type to another. Returns some Object Takes a single parameter Let’s see what it looks like when we use map in a stream pipeline. The lambda body can return an object of any type. By calling getGenre on the song, the stream after this point will be a stream of (genre) Strings.

```java
[Electronic, R&B, Rock, Soft Rock, Industri­
al Rock, Electronic, Soft Rock, Electronic,
Alternative Rock, Rock, Blues rock, Rock,
Rock, Industrial Rock, Electronic, R&B, Pop,
Pop, Alternative Rock, Latin, Latin, Rock]
```

The map’s lambda expression is similar to the one for filter; it takes a song and turns it into something else. Instead of returning a boolean, it returns some other object, in this case a String containing the song’s genre. File Edit Window Help RoadToNowhere %java JukeboxStreams unique elements

## Removing duplicates

```java
.stream()
.map( )
```

We’ve got a list of all the genres in our test data, but Lou probably doesn’t want to wade through all these duplicate genres. The map operation on its own will result in an out­ put List that’s the same size as the input List. Since stream operations are designed to be stacked together, perhaps there’s another operation we can use to get just one of every element in the stream? The output of this stream

```java
.distinct()
.collect(toList)
```

```java
List<String> genres = songs.stream()
.map(song -> song.getGenre())
.distinct()
.collect(Collectors.toList());
```

## Only one of every genre

```java
[Electronic, R&B, Rock, Soft Rock,
Industrial Rock, Alternative Rock,
Blues rock, Pop, Latin]
```

```java
String songTitle = "With a Little Help from My Friends";
List<String> result = allSongs.stream()
.filter(song -> song.getTitle().equals(songTitle))
.map(song -> song.getArtist())
.filter(artist -> !artist.equals("The Beatles"))
.collect(Collectors.toList());
```

## Sometimes you don’t even need a lambda expression

```java
Function<Song, String> getGenre = song -> song.getGenre();
```

```java
Function<Song, String> getGenre = Song::getGenre;
```

Method references can replace lambda expressions in a number of different cases. Generally, we might use a method reference if it makes the code easier to read. Take our old friend the Comparator, for example. There are a lot of helper methods on the Comparator interface that, when combined with a method reference, let you see which value is being used for sorting and in which direction. Instead of doing this, to order the songs from oldest to newest:

```java
List<Song> result = allSongs.stream()
.sorted((o1, o2) -> o1.getYear() - o2.getYear())
.collect(toList());
```

```java
List<Song> result = allSongs.stream()
.sorted(Comparator.comparingInt(Song::getYear))
.collect(toList());
```

Use a method reference combined with a static helper method from Comparator to state what the comparison should be: Method references can replace lambda expressions, but you don’t have to use them. Sometimes method references make the code easier to understand.  You don’t need to use method references if you don’t feel comfortable with them. What’s important is to be able to recognize the “::” syntax, especially in a stream pipeline.

## Collecting results in different ways

While Collectors.toList is the most commonly used Collector, there are other useful Collectors. For example, instead of using distinct to solve the last challenge, we could collect the results into a Set, which does not allow duplicates. The advantage of using this approach is that anything else that uses the results knows that because it’s a Set, by definition there will be no duplicates. 0 1 2 3 List

```java
Set<String> genres = songs.stream()
.map(song -> song.getGenre())
.collect(Collectors.toSet());
```

## But wait, there’s more!

```java
boolean result =
songs.stream()
.anyMatch(s -> s.getGenre().equals("R&B"));
boolean anyMatch(Predicate p);
boolean allMatch(Predicate p);
boolean noneMatch(Predicate p);
```

Collecting the results is not the only game in town; collect is just one of many terminal operations. terminal operations Checking if something exists You can use terminal operations that return a boolean value to look for certain things in the stream. For example, we can see if any R&B songs have been played in the diner. Find a specific thing Terminal operations that return an Optional value look for certain things in the stream. For example,

```java
Optional<Song> result =
songs.stream()
.filter(s -> s.getYear() == 1995)
.findFirst();
Optional<T> findAny();
Optional<T> findFirst();
Optional<T> max(Comparator c);
Optional<T> min(Comparator c);
Optional<T> reduce(BinaryOperator a);
```

```java
long result =
songs.stream()
.map(Song::getArtist)
.distinct()
.count();
long count();
```

There’s a count operation that you can use to find out the number of elements in your stream. We could find the number of unique artists, for example. There are even more terminal operations, and some of them depend upon the type of Stream you’re working with. Remember, the API documentation can help you figure out if there’s a built-in operation that does what you want. lambdas andstreams Wait a minute. How can a result be “Optional”? What does

```java
IceCream iceCream =
getIceCream("Strawberry");
```

result is to return an Optional. This is an object that wraps the result, so you can ask “Did I get a result? Or is it empty?” Then you can make a decision about what to do next.

## Optional is a wrapper

```java
Optional<IceCream> optional =
getIceCream("Strawberry");
if (optional.isPresent()) {
IceCream ice = optional.get();
}
```

```java
Optional<IceCream> optional =
getIceCream("Strawberry");
if (optional.isPresent()) {
} else {
System.out.println("No ice
cream for you!");
}
```

## Don’t forget to talk to the Optional wrapper

```java
%java OptionalExamples
Exception in thread "main" java.util.No­
SuchElementException: No value present
at java.base/java.util.Optional.
get(Optional.java:148)
at ch10c.OptionalExamples.
main(OptionalExamples.java:11)
Optional<IceCream> optional =
getIceCream("Strawberry");
IceCream ice = optional.get();
```

In the afternoons, Alex wanted the machine to give her the weakest coffee it had available (she had enough to keep her up at night; she didn’t need caffeine adding to her problems!). As an experienced software developer, she knew the Streams API would give her the best stream of coffee at the right time. The coffees would automatically be sorted from the weakest to the strongest using natural ordering, so she gave the coffee machine these instructions:

```java
Optional<String> afternoonCoffee = coffees.stream()
.map(Coffee::getName)
.sorted()
.findFirst();
```

The very next day, she asked for an afternoon coffee. To her horror, the machine presented her with an Americano, not the Decaf Cappuccino she was expecting. “I can’t drink that!! I’ll be up all night worrying about my latest software project!” What happened? Why did the coffee machine give Alex an Americano? Five-Minute Mystery The Unexpected Coffee Answers on page 419. the pool and place them into the blank

```java
%java StreamPuzzle
[Immigrant Song, With a Little
Help from My Friends, Hallucinate,
Pasos de cero, Cassidy]
With a Little Help from My Friends
No songs found by: The Beach Boys
```

```java
public class StreamPuzzle {
public static void main(String[] args) {
SongSearch songSearch = _____________;
songSearch.___________;
__________.search("The Beatles");
________________________________;
}
}
class _____________ {
private final List<Song> songs =
new JukeboxData.Songs().getSongs();
void printTopFiveSongs() {
List<String> topFive = songs.stream()
.______________
.______________
.______________
.collect(_________);
System.out.println(topFive);
}
void search(String artist) {
________ = songs.stream()
._______________
._______________;
if (_______________) {
System.out.println(______________);
} else {
System.out.println(______________);
}
}
}
```

```java
for (int i = 1; i < nums.size(); i++)
output += nums.get(i) + " ";
```

```java
for (int i = 0; i <= nums.size(); i++)
output += nums.get(i) + " ";
for (int i = 0; i <= nums.length; i++)
output += nums.get(i) + " ";
for (Integer num : nums)
output += nums + " ";
Compiler error
2 3 4 5
Exception thrown
[1, 2, 3, 4, 5]
[1, 2, 3, 4, 5]
[1, 2, 3, 4, 5]
[1, 2, 3, 4, 5]
[1, 2, 3, 4, 5]
1 2 3 4 5
```

```java
[Americano, Cappuccino,
Cortado, Espresso]
import java.util.*;
import java.util.stream.*;
public class CoffeeOrder {
public static void main(String[] args) {
List<String> coffees = List.of("Cappuccino",
"Americano", "Espresso", "Cortado", "Mocha",
"Cappuccino", "Flat White", "Latte");
List<String> coffeesEndingInO = coffees.stream()
.filter(s -> s.endsWith("o"))
.sorted()
.distinct()
.collect(Collectors.toList());
System.out.println(coffeesEndingInO);
}
}
```

coffee objects to a stream of Strings, and then ordered that. Strings are naturally ordered alphabetically, so when the coffee machine got the “first” of these results for Alex’s afternoon coffee, it was brewing a fresh “Americano.” If Alex wanted to order the coffees by strength, with the weakest (1 out of 5) first, she needed to order the stream of coffees first, before mapping it to a String name, afternoonCoffee = coffees.stream() .sorted()

```java
.map(Coffee::getName)
.findFirst();
```

```java
BiPredicate
ActionListener
Function
SocketOption
```

```java
Iterator
```

```java
public class StreamPuzzle {
```