# Chapter 11: Chapter 11: Data Structures

pages 347-406

your data without having to write your own sort algorithms (unless you’re reading this right now sitting in your Computer Science 101 class, in which case, trust us—you are SO going to be writing sort code while the rest of us just call a method in the Java API). In this chapter, you’re going to get a peek at when Java can save you some typing and figure out the types that you need. The Java Collections Framework has a data structure that should work for virtually anything

you’ll ever need to do. Want to keep a list that you can easily keep adding to? Want to find something by name? Want to create a list that automatically takes out all the duplicates? Sort your co-workers by the number of times they’ve tried to speak with their mic muted on a video call? Sort your pets by number of tricks learned? It’s all here... Data Structures 11collections and generics Sheesh... and all this time I could have just let Java put things in

generate reports, and manipulate the playlists. You’re not writing the entire app—some of the other software developers are involved as well, but you’re responsible for managing and sorting the data inside the Java app. And since Lou has a thing against databases, this is strictly an in- memory data collection. Another programmer will be writing the code to read the song data from a file and put the songs into a List. (In a few chapters you’ll learn how to read data from files, and write data to files.) All you’re going to get is a List with the song data the jukebox keeps adding to.

## Tracking song popularity on your jukebox <!--p348-->

```java
class MockSongs {
public static List<String> getSongStrings() {
List<String> songs = new ArrayList<>();
songs.add("somersault");
songs.add("cassidy");
songs.add("$10");
songs.add("havana");
songs.add("Cassidy");
songs.add("50 Ways");
return songs;
}
}
```

## Your first job, sort the songs in alphabetical order <!--p349-->

```java
import java.util.*;
public class Jukebox1 {
public static void main(String[] args) {
new Jukebox1().go();
}
public void go() {
List<String> songList = MockSongs.getSongStrings();
System.out.println(songList);
}
}
// Below is the "mock" code. A stand in for the actual
// I/O code that the other programmer will provide later
class MockSongs {
public static List<String> getSongStrings() {
List<String> songs = new ArrayList<>();
songs.add("somersault");
songs.add("cassidy");
songs.add("$10");
songs.add("havana");
songs.add("Cassidy");
songs.add("50 Ways");
return songs;
}
}
```

```java
%java Jukebox1
[somersault, cassidy, $10, havana,
Cassidy, 50 Ways]
```

## Great question! You spotted the diamond operator <!--p350-->

```java
ArrayList<String> songs = new ArrayList<String>();
```

```java
ArrayList<String> songs = new ArrayList<>();
```

```java
ArrayList<String> songs;
// lots of code between these lines...
```

## Exploring the java.util API, List and Collections <!--p352-->

We know that with an ArrayList, or any List, the elements are kept in the order in which they were added. So we’re going to need to sort the elements in the song list. In this chapter, we’ll be looking at some of the most important and commonly used collection classes in the java.util package, but for now, let’s limit ourselves to two classes: java.util.List and java.util.Collections. We’ve been using ArrayList for a while now. Because ArrayList IS-A List and because many of the methods we’re familiar with on ArrayList come from List, we can comfortably transfer most of what we know about working with ArrayLists to List.

The Collections class is known as a “utility” class. It’s a class that has a lot of handy methods for working with the various collection types. Excerpts from the API java.util.List sort(Comparator): Sorts this list according to the order induced by the specified Comparator. java.util.Collections sort(List): Sorts the specified list into ascending order, according to the natural ordering of its elements.

sort(List, Comparator): Sorts the specified list according to the order defined by the Comparator. We don’t always want our lists sorted alphabetically. We might want to sort clothes by size, or movies by how many five-star reviews they get. Java lets you sort the good old-fashioned way, alphabetically, and it also lets you create your own custom sorting approaches. Those references you see above to “Comparator” have to do with custom sorting, which we’ll get to later this chapter. So for now, let’s stick with “natural ordering” (alphabetical).

Since we know we have a List, it looks like we’ve found the perfect method, Collections.sort(). In the “Real-World”™ there are lots of ways to sort ArrayList API collections with generics

## “Natural Ordering,” what Java means by alphabetical <!--p353-->

Lou wants you to sort songs “alphabetically,” but what exactly does that mean? The A–Z part is obvious, but how about lowercase versus uppercase letters? How about numbers and special characters? Well, this is another can-of-worms topic, but Java uses Unicode, and for many of us in “the West” that means that numbers sort before uppercase letters, uppercase letters sort before lowercase letters, and some special characters sort before numbers and some sort after numbers. That’s pretty clear, right? Ha! Well, the upshot is that, by default, sorting in Java happens in what’s called “natural order,” which is more or less alphabetical. Let’s take a look at what happens when we sort our list of songs:

```java
public void go() {
List<String> songList = MockSongs.getSongStrings();
System.out.println(songList);
Collections.sort(songList);
System.out.println(songList);
}
}
```

```java
%java Jukebox1
[somersault, cassidy, $10, havana, Cassidy, 50 Ways]
[$10, 50 Ways, Cassidy, cassidy, havana, somersault]
```

## But now you need Song objects, not just simple Strings <!--p354-->

Now your boss Lou wants actual Song class instances in the list, not just Strings, so that each Song can have more data. The new jukebox device outputs more information, so the actual song file will have three pieces of information for each song. The Song class is really simple, with only one interesting feature—the overridden toString() method. Remember, the toString() method is defined in class Object, so every class in Java inherits the method. And since the toString() method is called on an object when it’s printed (System.out.println(anObject)), you should override it to print something more readable than the default unique identifier code. When you print a list, the toString() method will be called on each object.

```java
class SongV2 {
private String title;
private String artist;
private int bpm;
SongV2(String title, String artist, int bpm) {
this.title = title;
this.artist = artist;
this.bpm = bpm;
}
public String getTitle() {
return title;
}
public String getArtist() {
return artist;
}
public int getBpm() {
return bpm;
}
public String toString() {
return title;
}
}
```

```java
class MockSongs {
public static List<String> getSongStrings() { ... }
public static List<SongV2> getSongsV2() {
List<SongV2> songs = new ArrayList<>();
songs.add(new SongV2("somersault", "zero 7", 147));
songs.add(new SongV2("cassidy", "grateful dead", 158));
songs.add(new SongV2("$10", "hitchhiker", 140));
songs.add(new SongV2("havana", "cabello", 105));
songs.add(new SongV2("Cassidy", "grateful dead", 158));
songs.add(new SongV2("50 ways", "simon", 102));
return songs;
}
}
```

```java
import java.util.*;
public class Jukebox2 {
public static void main(String[] args) {
new Jukebox2().go();
}
public void go() {
List<SongV2> songList = MockSongs.getSongsV2();
System.out.println(songList);
Collections.sort(songList);
System.out.println(songList);
}
}
```

## It won’t compile! <!--p356-->

```java
%javac Jukebox2.java
Jukebox2.java:13: error: no suitable method found for
sort(List<SongV2>)
Collections.sort(songList);
^
...
1 error
```

## The sort() method declaration <!--p357-->

From the API docs (looking up the java.util.Collections class and scrolling to the sort() method), it looks like the sort() method is declared...strangely. Or at least different from anything we’ve seen so far. That’s because the sort() method (along with other things in the whole collection framework in Java) makes heavy use of generics. Any time you see something with angle brackets in Java source code or documentation, it means generics—a feature added in Java 5. So it looks like we’ll have to learn how to interpret the documentation before we can figure out why we were able to sort String objects in a List, but not a List of Song objects.

## Generics means more type-safety <!--p358-->

## Learning generics <!--p359-->

```java
new ArrayList<Song>()
<Song>()
List<Song> songList =
new ArrayList<Song>()
void foo(List<Song> list)
x.foo(songList)
```

## Using generic CLASSES <!--p360-->

```java
public boolean add(E o)
// more code
public class ArrayList<E> extends AbstractList<E> implements List<E> ... {
}
```

```java
public boolean add(E o)
// more code
public class ArrayList<E> extends AbstractList<E> ... {
}
```

## Using type parameters with ArrayList <!--p361-->

```java
List<String> thisList = new ArrayList<>
public boolean add(String o)
// more code
}
```

```java
public class ArrayList<String> extends AbstractList<String>... {
```

In other words, the “E” is replaced by the real type (also called the type parameter) that you use when you create the ArrayList. And that’s why the add() method for ArrayList won’t let you add anything except objects of a reference type that’s compatible with the type of “E.” So if you make an ArrayList<String>, the add() method suddenly becomes add(String o). If you make the ArrayList of type Dog, suddenly the add() method becomes add(Dog o).

see single letter used. Another convention is to use “T” (“Type”) unless you’re specifically writing a collection class, where you’d use “E” to represent the “type of the Element the collection will hold.” Sometimes you’ll see “R” for “Return type.”

## Using generic METHODS <!--p362-->

```java
public boolean add(E o)
public class ArrayList<E> extends AbstractList<E> ... {
```

```java
public <T extends Animal> void takeThing(ArrayList<T> list)
```

## Here’s where it gets weird... <!--p363-->

```java
public <T extends Animal> void takeThing(ArrayList<T> list)
```

```java
public void takeThing(ArrayList<Animal> list)
```

```java
%javac Jukebox2.java
Jukebox2.java:13: error: no suitable method found
for sort(List<SongV2>)
Collections.sort(songList);
^
...
1 error
import java.util.*;
public class Jukebox2 {
public static void main(String[] args) {
new Jukebox2().go();
}
public void go() {
List<SongV2> songList = MockSongs.getSongsV2();
System.out.println(songList);
Collections.sort(songList);
System.out.println(songList);
}
}
```

```java
public static <T extends Comparable<? super T>> void sort(List<T> list)
```

## Revisiting the sort() method <!--p365-->

```java
public final class String
implements java.io.Serializable, Comparable<String>, CharSequence {
```

```java
public static <T extends Comparable<? super T>> void sort(List<T> list)
```

```java
public interface Comparable<T> {
int compareTo(T o);
}
```

```java
a negative integer if this object is
less than the specified object;
a zero if they’re equal;
a positive integer if this object is
greater than the specified object.
```

## The new, improved, comparable Song class <!--p368-->

```java
[somersault, cassidy, $10, havana, Cassidy, 50
ways]
[$10, 50 ways, Cassidy, cassidy, havana, somer­
sault]
```

```java
class SongV3 implements Comparable<SongV3> {
private String title;
private String artist;
private int bpm;
public int compareTo(SongV3 s) {
return title.compareTo(s.getTitle());
}
SongV3(String title, String artist, int bpm) {
this.title = title;
this.artist = artist;
this.bpm = bpm;
}
public String getTitle() {
return title;
}
public String getArtist() {
return artist;
}
public int getBpm() {
return bpm;
}
public String toString() {
return title;
}
}
```

## We can sort the list, but... <!--p369-->

```java
java.util.Collections
```

```java
java.util.List
```

sort(List): Sorts the specified list into ascending order, according to the natural ordering of its elements. sort(List, Comparator): Sorts the specified list according to the order induced by the specified Comparator. sort(Comparator): Sorts this list according to the order induced by the specified Comparator. Note to self: figure out how to get/make a Comparator that can compare and order the songs by artist instead of title.

## Using a custom Comparator <!--p370-->

```java
public interface Comparator<T> {
int compare(T o1, T o2);
}
```

```java
import java.util.*;
public class Jukebox4 {
public static void main(String[] args) {
new Jukebox4().go();
}
public void go() {
List<SongV3> songList = MockSongs.getSongsV3();
System.out.println(songList);
Collections.sort(songList);
System.out.println(songList);
ArtistCompare artistCompare = new ArtistCompare();
songList.sort(artistCompare);
System.out.println(songList);
}
}
class ArtistCompare implements Comparator<SongV3> {
public int compare(SongV3 one, SongV3 two) {
return one.getArtist().compareTo(two.getArtist());
}
}
```

## Updating the Jukebox to use a Comparator <!--p371-->

```java
[somersault, cassidy, $10, havana, Cassidy, 50 ways]
[$10, 50 ways, Cassidy, cassidy, havana, somersault]
[havana, Cassidy, cassidy, $10, 50 ways, somersault]
```

```java
Collections.sort(myArrayList);
```

```java
Collections.sort(myArrayList, myCompare);
myArrayList.sort(myCompare);
```

2. What method must the class of the objects stored in myArrayList implement? ________________ 3. Can the class of the objects stored in myArrayList implement both Comparator AND Comparable? ________________ Given the following compilable statements (they both do the same thing): 4. Can the class of the objects stored in myArrayList implement Comparable? ________________ 5. Can the class of the objects stored in myArrayList implement Comparator? ________________

6. Must the class of the objects stored in myArrayList implement Comparable? ________________ 7. Must the class of the objects stored in myArrayList implement Comparator? ________________ 8. What must the class of the myCompare object implement? ________________ 9. What method must the class of the myCompare object implement? __________________ Possible Answers: Comparator, Comparable, compareTo( ),

## But wait! We’re sorting in two different ways! <!--p373-->

```java
public void go() {
List<SongV3> songList = MockSongs.getSongsV3();
System.out.println(songList);
Collections.sort(songList);
System.out.println(songList);
ArtistCompare artistCompare = new ArtistCompare();
songList.sort(artistCompare);
System.out.println(songList);
}
```

2. Using songLists.sort(artistCompare) because the ArtistCompare class implements Comparator While our new code allows us to sort songs by title and by artist, it is reminiscent of Frankenstein’s monster, cobbled together bit by bit. This uses Comparable to sort This uses a custom Comparator to sort A better approach would be to handle all of the sorting definitions in classes that implement Comparator.

## Sorting using only Comparators <!--p374-->

```java
public class Jukebox5 {
public static void main(String[] args) {
new Jukebox5().go();
}
public void go() {
List<SongV3> songList = MockSongs.getSongsV3();
System.out.println(songList);
TitleCompare titleCompare = new TitleCompare();
songList.sort(titleCompare);
System.out.println(songList);
ArtistCompare artistCompare = new ArtistCompare();
songList.sort(artistCompare);
System.out.println(songList);
}
}
class TitleCompare implements Comparator<SongV3> {
public int compare(SongV3 one, SongV3 two) {
return one.getTitle().compareTo(two.getTitle());
}
}
class ArtistCompare implements Comparator<SongV3> {
public int compare(SongV3 one, SongV3 two) {
return one.getArtist().compareTo(two.getArtist());
}
}
// more specialized Comparator classes could go here,
// e.g. BpmCompare
```

Having Song implement Comparable and creating a custom Comparator for sorting by Artist absolutely works, but it’s confusing to rely on two different mechanisms for our sort. It’s much clearer if our code uses the same technique to sort, regardless of how Lou wants his songs sorted. The code below has been updated to use Comparators for sorting by both Title and Artist; the new code is in bold. collections with generics

```java
songList.sort(new Comparator<SongV3>() {
public int compare(SongV3 one, SongV3 two) {
return one.getTitle().compareTo(two.getTitle());
}
});
```

of the Comparator classes we wrote for Lou. The first thing to notice is that all we really want to sort our collection is the one line of code in the middle of the class. The rest of the code is just the long-winded syntax that’s necessary to let the compiler know what type of class this is and which method it implements.

## Just the code that matters <!--p375-->

```java
class TitleCompare implements Comparator<Song> {
public int compare(Song one, Song two) {
return one.getTitle().compareTo(two.getTitle());
}
}
```

## What do we REALLY need in order to sort? <!--p376-->

```java
public class Jukebox5 {
public void go() {
List<SongV3> songList = MockSongs.getSongsV3();
...
TitleCompare titleCompare = new TitleCompare();
songList.sort(titleCompare);
...
}
}
class TitleCompare implements Comparator<SongV3> {
public int compare(SongV3 one, SongV3 two) {
return one.getTitle().compareTo(two.getTitle());
}
}
```

```java
...
songList.sort(titleCompare);
...
class TitleCompare implements Comparator<Song> {
public int compare(Song one, Song two) {
return one.getTitle().compareTo(two.getTitle());
}
}
...
```

## Enter lambdas! Leveraging what the compiler can infer <!--p378-->

```java
songList.sort((one, two) -> one.getTitle().compareTo(two.getTitle()));
```

## Where did all that code go? <!--p379-->

## Updating the Jukebox code with lambdas <!--p380-->

```java
import java.util.*;
public class Jukebox6 {
public static void main(String[] args) {
new Jukebox6().go();
}
public void go() {
List<SongV3> songList = MockSongs.getSongsV3();
System.out.println(songList);
songList.sort((one, two) -> one.getTitle().compareTo(two.getTitle()));
System.out.println(songList);
songList.sort((one, two) -> one.getArtist().compareTo(two.getArtist()));
System.out.println(songList);
}
}
%java Jukebox6
[somersault, cassidy, $10, havana, Cassidy, 50 ways]
[$10, 50 ways, Cassidy, cassidy, havana, somersault]
[havana, Cassidy, cassidy, $10, 50 ways, somersault]
```

```java
import __________________;
public class SortMountains {
public static void main(String [] args) {
new SortMountains().go();
}
public void go() {
List______________ mountains = new ArrayList<>();
mountains.add(new Mountain("Longs", 14255));
mountains.add(new Mountain("Elbert", 14433));
mountains.add(new Mountain("Maroon", 14156));
mountains.add(new Mountain("Castle", 14265));
System.out.println("as entered:\n" + mountains);
mountains._______(____->____________);
System.out.println("by name:\n" + mountains);
_________._______(____->____________);
System.out.println("by height:\n" + mountains);
}
}
class Mountain {
__________________;
_________________;
______________________ {
_________________;
_________________;
}
_________________________ {
______________________________;
}
}
```

```java
as entered:
[Longs 14255, Elbert 14433, Maroon 14156, Castle 14265]
by name:
[Castle 14265, Elbert 14433, Longs 14255, Maroon 14156]
by height:
[Elbert 14433, Castle 14265, Longs 14255, Maroon 14156]
```

## Uh-oh. The sorting all works, but now we have duplicates... <!--p382-->

The sorting works great; now we know how to sort on both title and artist. But there’s a new problem we didn’t notice with a test sample of the jukebox songs—the sorted list contains duplicates. Unlike the mock code, Lou’s real jukebox application appears to just keep writing to the file regardless of whether the same song has already been played (and thus written) to the text file. The SongListMore.txt jukebox text file is an example. It’s a complete record of every song that was played,

```java
[somersault: zero 7, cassidy: grateful dead, $10: hitchhiker,
havana: cabello, $10: hitchhiker, cassidy: grateful dead, 50
ways: simon]
[$10: hitchhiker, $10: hitchhiker, 50 ways: simon, cassidy:
grateful dead, cassidy: grateful dead, havana: cabello,
somersault: zero 7]
[havana: cabello, cassidy: grateful dead, cassidy: grateful
dead, $10: hitchhiker, $10: hitchhiker, 50 ways: simon,
somersault: zero 7]
```

```java
somersault, zero 7, 147
cassidy, grateful dead, 158
$10, hitchhiker, 140
havana, cabello, 105
$10, hitchhiker, 140
cassidy, grateful dead, 158
50 ways, simon, 102
```

## We need a Set instead of a List <!--p383-->

## The Collection API (part of it) <!--p384-->

We updated the Jukebox code to put the songs in a HashSet to try to eliminate our duplicate songs. (Note: we left out some of the Jukebox code, but you can copy it from earlier versions.)

## Using a HashSet instead of ArrayList <!--p385-->

```java
import java.util.*;
public class Jukebox8 {
public static void main(String[] args) {
new Jukebox8().go();
}
public void go() {
List<SongV3> songList = MockMoreSongs.getSongsV3();
System.out.println(songList);
songList.sort((one, two) -> one.getTitle().compareTo(two.getTitle()));
System.out.println(songList);
Set<SongV3> songSet = new HashSet<>(songList);
System.out.println(songSet);
}
}
```

```java
[somersault, cassidy, $10, havana, $10, cassidy, 50 ways]
[$10, $10, 50 ways, cassidy, cassidy, havana, somersault]
[$10, 50 ways, havana, cassidy, $10, cassidy, somersault]
```

## What makes two objects equal? <!--p386-->

```java
if (song1 == song2) {
// both references are referring
// to the same object on the heap
}
if (song1.equals(song2) && song1.hashCode() == song2.hashCode()) {
// both references are referring to either a
// a single object, or to two objects that are equal
}
```

## How a HashSet checks for duplicates: hashCode() and equals() <!--p387-->

```java
class SongV4 implements Comparable<SongV4> {
private String title;
private String artist;
private int bpm;
public boolean equals(Object aSong) {
SongV4 other = (SongV4) aSong;
return title.equals(other.getTitle());
}
public int hashCode() {
return title.hashCode();
}
public int compareTo(SongV4 s) {
return title.compareTo(s.getTitle());
}
SongV4(String title, String artist, int bpm) {
this.title = title;
this.artist = artist;
this.bpm = bpm;
}
public String getTitle() {
return title;
}
public String getArtist() {
return artist;
}
public int getBpm() {
return bpm;
}
public String toString() {
return title;
}
}
```

```java
%java Jukebox9
[somersault, cassidy, $10, havana, $10,
cassidy, 50 ways]
[$10, $10, 50 ways, cassidy, cassidy, havana,
somersault]
[havana, $10, 50 ways, cassidy, somersault]
```

```java
public class Jukebox10 {
public static void main(String[] args) {
new Jukebox10().go();
}
public void go() {
List<SongV4> songList = MockMoreSongs.getSongsV4();
System.out.println(songList);
songList.sort((one, two) -> one.getTitle().compareTo(two.getTitle()));
System.out.println(songList);
Set<SongV4> songSet = new TreeSet<>(songList);
System.out.println(songSet);
}
}
```

TreeSet is similar to HashSet in that it prevents duplicates. But it also keeps the list sorted. It works just like the sort() method in that if you make a TreeSet without giving it a Comparator, the TreeSet uses each object’s compareTo() method for the sort. But you have the option of passing a Comparator to the TreeSet constructor, to have the TreeSet use that instead. The downside to TreeSet is that if you don’t need sorting, you’re still paying for it with a small performance

```java
Set<SongV4> songSet = new TreeSet<>((o1, o2) -> o1.getBpm() - o2.getBpm());
songSet.addAll(songList);
```

## What you MUST know about TreeSet... <!--p391-->

```java
import java.util.*;
public class TestTree {
public static void main(String[] args) {
new TestTree().go();
}
public void go() {
Book b1 = new Book("How Cats Work");
Book b2 = new Book("Remix your Body");
Book b3 = new Book("Finding Emo");
Set<Book> tree = new TreeSet<>();
tree.add(b1);
tree.add(b2);
tree.add(b3);
System.out.println(tree);
}
}
class Book {
private String title;
public Book(String t) {
title = t;
}
}
```

3. If there is a problem (either compile-time or runtime) with this code, how would you fix it? TreeSet looks easy, but make sure you really understand what you need to do to Answers on page 366.

## TreeSet elements MUST be comparable <!--p392-->

```java
class Book implements Comparable<Book> {
private String title;
public Book(String t) {
title = t;
}
public int compareTo(Book other) {
return title.compareTo(other.title);
}
}
```

```java
class BookCompare implements Comparator<Book> {
public int compare(Book one, Book two) {
return one.title.compareTo(two.title);
}
}
public class TestTreeComparator {
public void go() {
Book b1 = new Book("How Cats Work");
Book b2 = new Book("Remix your Body");
Book b3 = new Book("Finding Emo");
BookCompare bookCompare = new BookCompare();
Set<Book> tree = new TreeSet<>(bookCompare);
tree.add(b1);
tree.add(b2);
tree.add(b3);
System.out.println(tree);
}
}
```

## We’ve seen Lists and Sets, now we’ll use a Map <!--p393-->

Lists and Sets are great, but sometimes a Map is the best collection (not Collection with a capital “C”—remember that Maps are part of Java collections but they don’t implement the Collection interface). Imagine you want a collection that acts like a property list, where you give it a name and it gives you back the value associated with that name. Keys can be any Java object (or, through autoboxing, a primitive), but you’ll often see String keys (i.e., property names) or Integer keys (representing unique IDs, for example).

```java
public class TestMap {
public static void main(String[] args) {
Map<String, Integer> scores = new HashMap<>();
scores.put("Kathy", 42);
scores.put("Bert", 343);
scores.put("Skyler", 420);
System.out.println(scores);
System.out.println(scores.get("Bert"));
}
}
```

```java
%java TestMap
{Skyler=420, Bert=343, Kathy=42}
```

```java
List<String> songs = new ArrayList<>();
songs.add("somersault");
songs.add("cassidy");
songs.add("$10");
```

```java
List<String> songs = new ArrayList<>();
songs.add("somersault");
songs.add("cassidy");
songs.add("$10");
return Collections.unmodifiableList(songs);
```

start, and then we don’t intend to change it at all during the lifetime of the collection. If we wanted to really make sure that no-one changed the collection after we’d created it, we’d have to add an extra step: That’s a lot of code! And it’s a lot of code for something common that we probably want to do a lot. Fortunately for us, Java now has “Convenience Factory Methods of Collections” (they were added in Java 9). We can use these methods to create common data structures and fill them with data, with just one method call.

```java
List<String> strings = List.of("somersault", "cassidy", "$10");
```

```java
List<SongV4> songs = List.of(new SongV4("somersault", "zero 7", 147),
new SongV4("cassidy", "grateful dead", 158),
new SongV4("$10", "hitchhiker", 140));
```

```java
Set<Book> books = Set.of(new Book("How Cats Work"),
new Book("Remix your Body"),
new Book("Finding Emo"));
```

To create the list of Strings from the last page, we don’t need five lines of code; we just need one: If you want to add Song objects instead of simple Strings, it’s still short and descriptive: Creating a Set: Set.of() Creating a Set uses very similar syntax: Creating a Map: Map.of(), Map.ofEntries() Maps are different, because they take two objects for each “entry”—a key and a value. If you want to put less than 10 entries into your Map, you can use Map.of, passing in key, value, key, value, etc.:

```java
Map<String, Integer> scores = Map.of("Kathy", 42,
"Bert", 343,
"Skyler", 420);
```

```java
Map<String, String> stores = Map.ofEntries(Map.entry("Riley", "Supersports"),
Map.entry("Brooklyn", "Camera World"),
Map.entry("Jay", "Homecase"));
```

If you have more than 10 entries, or if you want to be clearer about how your keys are paired up to their values, you can use Map.ofEntries instead: To make the line shorter, you can use a static import on Map.entry (we talked about static imports in Chapter 10). é é

## Convenience Factory Methods for Collections <!--p395-->

Convenience Factory Methods are just that—a convenience that will work for most of the cases where you want to create a collection prefilled with data. And for those cases where these factory methods don’t suit you, you can still use the Collections constructors and add() or put() methods instead. Convenience Factory Methods for Collections allow you to easily create a List, Set, or Map that’s been prefilled with known data. There are a couple of things to understand about using them:

## Finally, back to generics <!--p396-->

```java
public class TestGenerics1 {
public static void main(String[] args) {
List<Animal> animals = List.of(new Dog(), new Cat(), new Dog());
takeAnimals(animals);
}
public static void takeAnimals(List<Animal> animals) {
for (Animal a : animals) {
a.eat();
}
}
}
```

```java
%java TestGenerics1
animal eating
animal eating
animal eating
```

```java
abstract class Animal {
void eat() {
System.out.println("animal eating");
}
}
class Dog extends Animal {
void bark() { }
}
class Cat extends Animal {
void meow() { }
}
```

## But will it work with List<Dog>? <!--p397-->

```java
public void go() {
List<Animal> animals = List.of(new Dog(), new Cat(), new Dog());
takeAnimals(animals);
List<Dog> dogs = List.of(new Dog(), new Dog());
takeAnimals(dogs);
}
public void takeAnimals(List<Animal> animals) {
for (Animal a : animals) {
a.eat();
}
}
```

```java
%javac TestGenerics2.java
TestGenerics2.java:20: error: incompatible types:
List<Dog> cannot be converted to List<Animal>
takeAnimals(dogs);
^
1 error
```

## What could happen if it were allowed...? <!--p398-->

```java
public void takeAnimals(List<Animal> animals) {
for (Animal a : animals) {
a.eat();
}
}
```

```java
public void takeAnimals(List<Animal> animals) {
animals.add(new Cat());
}
```

## We can do this with wildcards <!--p399-->

```java
public void takeAnimals(List<? extends Animal> animals) {
for (Animal a : animals) {
a.eat();
}
}
```

## Using the method’s generic type parameter <!--p400-->

```java
public <T extends Animal> void takeAnimals(List<T> list) { }
```

```java
public <T extends Animal>List<T> takeAnimals(List<T> list) { }
```

```java
List<Dog> dogs = List.of(new Dog(), new Dog());
List<Dog> vaccinatedDogs = takeAnimals(dogs);
List<Animal> animals = List.of(new Dog(), new Cat());
List<Animal> vaccinatedAnimals = takeAnimals(animals);
```

Well, not much as the method stands right now, we don’t need to use “T” for anything. But if we made a change to our method to return a List, for example of all the animals we had success­ fully vaccinated, we can declare that the List that’s returned has the same generic type as the List that’s passed in: When you call the method, you know you’re going to get the same type back as you put in. The List we get back from the

```java
public void go() {
List<Dog> dogs = List.of(new Dog(), new Dog());
List<? extends Animal> vaccinatedSomethings = takeAnimals(dogs);
}
public List<? extends Animal> takeAnimals(List<? extends Animal> animals) { }
```

If the method used the wildcard for both method parameter and return type, there’s nothing to guarantee they’re the same type. In fact, anything calling the method has almost no idea what’s going to be in the collection, other than “some sort of animal.” Using the wildcard (“? extends”) is fine when you don’t care much about the generic type, you just want to allow all subtypes of some type. Using a type parameter (“T”) is more helpful when you want to do more with the type itself, for

```java
private void takeDogs(List<Dog> dogs) { }
private void takeAnimals(List<Animal> animals) { }
private void takeSomeAnimals(List<? extends Animal> animals) { }
private void takeObjects(ArrayList<Object> objects) { }
```

```java
Collections.sort(myArrayList);
```

```java
Collections.sort(myArrayList, myCompare);
```

2. What method must the class of the objects stored in myArrayList implement? compareTo( ) 3. Can the class of the objects stored in myArrayList implement both Comparator AND Comparable? yes Given the following compilable statement: 4. Can the class of the objects stored in myArrayList implement Comparable? yes 5. Can the class of the objects stored in myArrayList implement Comparator? yes 6. Must the class of the objects stored in myArrayList implement Comparable? no

```java
public class SortMountains {
public static void main(String[] args) {
new SortMountains().go();
}
public void go() {
mountains.add(new Mountain("Longs", 14255));
mountains.add(new Mountain("Elbert", 14433));
mountains.add(new Mountain("Maroon", 14156));
mountains.add(new Mountain("Castle", 14265));
System.out.println("as entered:\n" + mountains);
```

```java
System.out.println("by height:\n" + mountains);
}
}
class Mountain {
```

```java
}
}
```

```java
as entered:
[Longs 14255, Elbert 14433, Maroon 14156, Castle 14265]
by name:
[Castle 14265, Elbert 14433, Longs 14255, Maroon 14156]
by height:
[Elbert 14433, Castle 14265, Longs 14255, Maroon 14156]
```

```java
songList.sort((one, two) -> one.getBpm() - two.getBpm());
songList.sort((one, two) -> two.getTitle().compareTo(one.getTitle()));
```

```java
[50 ways, havana, $10, somersault, cassidy, Cassidy]
[somersault, havana, cassidy, Cassidy, 50 ways, $10]
```

```java
Exception in thread "main" java.lang.ClassCastException: class Book can­
not be cast to class java.lang.Comparable
at java.base/java.util.TreeMap.compare(TreeMap.java:1291)
at java.base/java.util.TreeMap.put(TreeMap.java:536)
at java.base/java.util.TreeSet.add(TreeSet.java:255)
at TestTree.go(TestTree.java:16)
at TestTree.main(TestTree.java:7)
```

3. If there is a problem (either compile-time or runtime) with this code, how would you fix it? It compiles correctly It throws an exception: Make Book implement Comparable, or pass the TreeSet a Comparator Sorting with lambdas (from page 342) See page 574 collections with generics (from page 363) Compiles? ❑ takeAnimals(new ArrayList<Animal>()); ❑ takeDogs(new ArrayList<Animal>()); ❑ takeAnimals(new ArrayList<Dog>()); ❑ takeDogs(new ArrayList<>()); ❑ List<Dog> dogs = new ArrayList<>(); takeDogs(dogs);