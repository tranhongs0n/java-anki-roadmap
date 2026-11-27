# Chapter 13: Chapter 13: Risky Behavior

pages 459-498

exceptional situation? So far in this book, we haven’t really taken any risks. We’ve certainly had things go wrong at runtime, but the problems were mostly flaws in our own code. Bugs. And those we should fix at development time. No, the problem-handling code we’re talking about here is for code that you can’t guarantee will work at runtime. Code that expects the file to be in the right directory, the server to be running, or the Thread to stay asleep. And we have to do

this now. Because in this chapter, we’re going to build something that uses the risky JavaSound API. We’re going to build a MIDI Music Player. Risky Behavior Sure, it’s risky, but I can handle it if something goes wrong. 422chapter 13 building the MIDI Music Player

## Let’s make a Music Machine

## We’ll start with the basics

## First we need a Sequencer

```java
import javax.sound.midi.*;
public class MusicTest1 {
public void play() {
try {
Sequencer sequencer = MidiSystem.getSequencer();
System.out.println("Successfully got a sequencer");
}
}
public static void main(String[] args) {
MusicTest1 mt = new MusicTest1();
mt.play();
}
}
```

that plays the music. A sequencer can do a lot of different things, but in this book, we’re using it strictly as a playback device. It’s like a device that streams music, but with a few added features. The Sequencer class is in the javax.sound.midi package. So let’s start by making sure we can make (or get) a Sequencer object. but it looked so simple import the javax.sound.midi package We need a Sequencer object. It’s

```java
% javac MusicTest1.java
MusicTest1.java:13: unreported exception javax.sound.midi.
MidiUnavailableException; must be caught or declared to be
thrown
Sequencer sequencer = MidiSystem.getSequencer();
^
1 errors
```

```java
void moo() {
if (serverDown) {
explode();
}
}
```

```java
class Cow {
void moo() {
if (serverDown){
explode();
}
}
}
```

```java
class Cow {
void moo() {
if (serverDown){
explode();
}
}
}
```

```java
class Cow {
void moo() {
if (serverDown){
explode();
}
}
}
```

```java
class Bar {
void go() {
moo();
}
int stuff() {
x.beep();
}
}
class Bar {
void go() {
try{
moo();
}catch(MX m){
cry();
}
}
}
```

situations” that pop up at runtime; it lets you put all your error-handling code in one easy-to- read place. It’s based on the method you’re calling telling you it’s risky (i.e., that the method might generate an exception), so that you can write code to deal with that possibility. If you know you might get an exception when you call a particular method, you can be prepared for—possibly even recover from—the problem that caused the exception.

So, how does a method tell you it might throw an exception? You find a throws clause in the risky method’s declaration. The getSequencer() method takes a risk. It can fail at runtime. So it must “declare” the risk you take when you call it. when things might go wrong Methods in Java use exceptions to tell the calling code, “Something Bad Happened. I failed.” Risky methods that could fail at runtime declare the exceptions that might happen using “throws SomeKindOfException” on their method declaration.

```java
import javax.sound.midi.*;
public class MusicTest1 {
public void play() {
try {
Sequencer sequencer = MidiSystem.getSequencer();
System.out.println("Successfully got a sequencer");
} catch(MidiUnavailableException e) {
System.out.println("Bummer");
}
}
public static void main(String[] args) {
MusicTest1 mt = new MusicTest1();
mt.play();
}
}
```

```java
try {
// do risky thing
} catch(Exception e) {
// try to recover
}
```

```java
public void takeRisk() throws BadException {
if (abandonAllHope) {
throw new BadException();
}
}
```

```java
public void crossFingers() {
try {
anObject.takeRisk();
} catch (BadException e) {
System.out.println("Aaargh!");
e.printStackTrace();
}
}
```

```java
class Cow {
void moo() {
if (serverDown){
explode();
}
}
}
```

```java
class Bar {
void go() {
moo();
}
int stuff() {
x.beep();
}
}
```

```java
throw new NoCaffeineException();
```

```java
try {
Foo f = x.doRiskyThing();
int b = f.getNum();
}catch(Exception e) {
System.out.println("failed");
}
System.out.println("We made it!");
```

```java
We made it!
```

## Flow control in try/catch blocks

```java
try {
Foo f = x.doRiskyThing();
int b = f.getNum();
}catch(Exception e) {
System.out.println("failed");
}
System.out.println("We made it!");
```

```java
failed
We made it!
```

```java
try{
turnOvenOn();
x.bake();
turnOvenOff();
}catch (BakingException e) {
e.printStackTrace();
turnOvenOff();
}
```

```java
try{
turnOvenOn();
x.bake();
}catch (BakingException e) {
e.printStackTrace();
}finally {
turnOvenOff();
}
```

```java
public class TestExceptions {
public static void main(String[] args) {
String test = "no";
try {
System.out.println("start try");
doRisky(test);
System.out.println("end try");
} catch (ScaryException se) {
System.out.println("scary exception");
} finally {
System.out.println("finally");
}
System.out.println("end of main");
}
static void doRisky(String test) throws ScaryException {
System.out.println("start risky");
if ("yes".equals(test)) {
throw new ScaryException();
}
System.out.println("end risky");
}
}
class ScaryException extends Exception {
}
```

```java
public class WashingMachine {
public void go() {
Laundry laundry = new Laundry();
try {
laundry.doLaundry();
} catch (PantsException pex) {
// recovery code
} catch (LingerieException lex) {
// recovery code
}
}
}
```

```java
public class Laundry {
public void doLaundry() throws PantsException, LingerieException {
// code that could throw either exception
}
}
```

## Exceptions are polymorphic

```java
public void doLaundry()throws ClothingException {
```

```java
try {
laundry.doLaundry();
} catch(ClothingException cex) {
// recovery code
}
try {
laundry.doLaundry();
} catch(ShirtException shex) {
// recovery code
}
```

```java
try {
laundry.doLaundry();
} catch(Exception ex) {
// recovery code...
}
```

```java
try {
laundry.doLaundry();
} catch (TeeShirtException tex) {
// recovery from TeeShirtException
} catch (LingerieException lex) {
// recovery from LingerieException
} catch (ClothingException cex) {
// recovery from all others
}
```

```java
catch(TeeShirtException tex)
catch(ShirtException sex)
catch(ClothingException cex)
```

```java
try {
laundry.doLaundry();
} catch(ClothingException cex) {
// recovery from ClothingException
} catch(LingerieException lex) {
// recovery from LingerieException
} catch(ShirtException shex) {
// recovery from ShirtException
}
```

```java
try {
x.doRisky();
} catch(AlphaEx a) {
// recovery from AlphaEx
} catch(BetaEx b) {
// recovery from BetaEx
} catch(GammaEx c) {
// recovery from GammaEx
} catch(DeltaEx d) {
// recovery from DeltaEx
}
```

```java
public void foo() throws ReallyBadException {
// call risky method without a try/catch
laundry.doLaundry();
}
```

```java
public class Washer {
Laundry laundry = new Laundry();
public void foo() throws ClothingException {
laundry.doLaundry();
}
public static void main (String[] args) throws ClothingException {
Washer a = new Washer();
a.foo();
}
}
```

## Handle or Declare. It’s the law.

```java
try {
laundry.doLaundry();
} catch(ClothingExceptioncex) {
// recovery code
}
```

```java
void foo() throws ClothingException {
laundry.doLaundry();
}
```

```java
public class Washer {
Laundry laundry = new Laundry();
public void foo() throws ClothingException {
laundry.doLaundry();
}
public static void main (String[] args) {
Washer a = new Washer();
a.foo();
}
}
```

```java
public void play() {
try {
Sequencer sequencer = MidiSystem.getSequencer();
System.out.println("Successfully got a sequencer");
} catch(MidiUnavailableException e) {
System.out.println("Bummer");
}
}
```

## Getting back to our music code...

```java
void go() {
Foo f = new Foo();
f.foof();
catch(FooException ex) { }
}
```

```java
try {
x.doStuff();
}
int y = 43;
} catch(Exception ex) { }
```

```java
try {
x.doStuff();
} finally {
// cleanup
}
```

```java
void go() throws FooException {
try {
x.doStuff();
} finally { }
}
```

## Code Kitchen

that MIDI data doesn’t actually create any sound that you hear. For sound to come out of the speakers, the MIDI data has to be sent through some kind of MIDI device that takes the MIDI instructions and renders them in sound, by triggering either a hardware in­ strument or a “virtual” instrument (software synthesizer). In this book, we’re using only software devices, so here’s how it works in JavaSound:

## Making actual sound

```java
Sequencer player = MidiSystem.getSequencer();
player.open();
Sequence seq = new Sequence(timing,4);
Track t = seq.createTrack();
t.add(myMidiEvent1);
player.setSequence(seq);
```

```java
player.start();
```

```java
import javax.sound.midi.*;
import static javax.sound.midi.ShortMessage.*;
public class MiniMiniMusicApp {
public static void main(String[] args) {
MiniMiniMusicApp mini = new MiniMiniMusicApp();
mini.play();
}
public void play() {
try {
Sequencer player = MidiSystem.getSequencer();
player.open();
Sequence seq = new Sequence(Sequence.PPQ, 4);
Track track = seq.createTrack();
ShortMessage msg1 = new ShortMessage();
msg1.setMessage(NOTE_ON, 1, 44, 100);
MidiEvent noteOn = new MidiEvent(msg1, 1);
track.add(noteOn);
ShortMessage msg2 = new ShortMessage();
msg2.setMessage(NOTE_OFF, 1, 44, 100);
MidiEvent noteOff = new MidiEvent(msg2, 16);
track.add(noteOff);
player.setSequence(seq);
player.start();
} catch (Exception e) {
e.printStackTrace();
}
}
}
```

## Version 1: Your very first sound player app

```java
ShortMessage msg = new ShortMessage();
```

## Making a MidiEvent (song data)

```java
msg.setMessage(144, 1, 44, 100);
```

```java
MidiEvent noteOn = new MidiEvent(a, 1);
```

```java
track.add(noteOn);
```

A MIDI message holds the part of the event that says what to do. It’s the actual instruction you want the sequencer to execute. The first argument of an instruction is always the type of the message. The values you pass to the other three arguments depend on the type of message. For example, a message of type 144 means “NOTE ON.” But in order to carry out a NOTE ON, the sequencer needs to know a few things. Imagine the sequencer saying, “OK, I’ll play a note, but which channel? In other words, do you want me to play a Drum note or a Piano note? And which note? Middle-C? D Sharp? And while we’re at it, at which velocity should I play the note?

To make a MIDI message, make a ShortMessage instance and invoke setMessage(), passing in the four arguments for the message. But remember, the message says only what to do, so you still need to stuff the message into an event that adds when that message should “fire.”

## MIDI message: the heart of a MidiEvent

```java
msg.setMessage(144, 1, 44, 100);
```

```java
msg.setMessage(128, 1, 44, 100);
MidiEvent noteOff = new MidiEvent(b, 3 );
```

## Change a message

```java
msg.setMessage(144, 1, 20, 100);
```

```java
first.setMessage(192, 1, 102, 0);
```

```java
import javax.sound.midi.*;
import static javax.sound.midi.ShortMessage.*;
public class MiniMusicCmdLine {
public static void main(String[] args) {
MiniMusicCmdLine mini = new MiniMusicCmdLine();
if (args.length < 2) {
System.out.println("Don’t forget the instrument and note args");
} else {
int instrument = Integer.parseInt(args[0]);
int note = Integer.parseInt(args[1]);
mini.play(instrument, note);
}
}
public void play(int instrument, int note) {
try {
Sequencer player = MidiSystem.getSequencer();
player.open();
Sequence seq = new Sequence(Sequence.PPQ, 4);
Track track = seq.createTrack();
ShortMessage msg1 = new ShortMessage();
msg1.setMessage(PROGRAM_CHANGE, 1, instrument, 0);
MidiEvent changeInstrument = new MidiEvent(msg1, 1);
track.add(changeInstrument);
ShortMessage msg2 = new ShortMessage();
msg2.setMessage(NOTE_ON, 1, note, 100);
MidiEvent noteOn = new MidiEvent(msg2, 1);
track.add(noteOn);
ShortMessage msg3 = new ShortMessage();
msg3.setMessage(NOTE_OFF, 1, note, 100);
MidiEvent noteOff = new MidiEvent(msg3, 16);
track.add(noteOff);
player.setSequence(seq);
player.start();
} catch (Exception ex) {
ex.printStackTrace();
}
}
}
```

```java
%java MiniMusicCmdLine 80 20
%java MiniMusicCmdLine 40 70
```

6. If you define a try block, you can pair it with a matching catch or finally block, or both. 7. If you write a method that declares that it can throw a compiler-checked exception, you must also wrap the exception throwing code in a try/catch block. 8. The main( ) method in your program must handle all unhandled exceptions thrown to it. 9. A single try block can have many different catch blocks. 10. A method can throw only one kind of exception.

```java
try {
public static void main(String [] args) {
String test = args[0];
System.out.print("o");
class MyEx extends Exception { }
public class ExTestDrive {
```

```java
% java ExTestDrive yes
thaws
% java ExTestDrive no
throws
if ("yes".equals(t)) {
System.out.print("r");
System.out.print("t");
static void doRisky(String t) throws MyEx {
System.out.print("h");
} catch (MyEx e) {
System.out.print("a");
System.out.print("w");
System.out.println("s");
doRisky(test);
} finally {
throw new MyEx();
```

```java
class MyEx extends Exception { }
public class ExTestDrive {
public static void main(String[] args) {
String test = args[0];
try {
System.out.print("t");
doRisky(test);
System.out.print("o");
} catch (MyEx e) {
System.out.print("a");
} finally {
System.out.print("w");
}
System.out.println("s");
}
static void doRisky(String t) throws MyEx {
System.out.print("h");
if ("yes".equals(t)) {
throw new MyEx();
}
System.out.print("r");
}
}
```

```java
% java ExTestDrive yes
thaws
% java ExTestDrive no
throws
```