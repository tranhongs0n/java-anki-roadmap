# Audit log

Mỗi mục: thẻ, phán quyết, lý do, hành động đã làm. Flag 2 là hàng đợi audit; flag 1 là hàng đợi giải thích.

## 2026-11-27

### Card 1795706077222 — deleted

**Card:** A loop counts letter 'p' by iterating characters; what happens if the `continue` is removed?
**Back:** The count becomes wrong, counting every character

Phán quyết: **delete** (không rewrite).

- Front tham chiếu một đoạn code chỉ có trong bài viết, không có trên thẻ — người học không thể dựng lại tình huống.
- Extra bị hỏng văn bản: "The original 9 'p's become 35 's example." — câu đứt giữa, không truyền đạt được gì.
- Sự kiện bên dưới ("continue bỏ phần còn lại của vòng lặp hiện tại") đã có 3 thẻ phủ: 1795706077221, 1795752249864, và hai thẻ break-vs-continue.
- Kiểu "chuyện gì xảy ra nếu xoá dòng này" chỉ kiểm tra một ví dụ cụ thể, không phải một quy tắc dùng lại được.

Hành động: xoá note khỏi Anki, xoá entry khỏi `cards/devjava-CHUNK-0.json` (đã verify `notesInfo` trả về rỗng, 0 card còn lại).

### Hàng đợi mở

- 1795706077234 + 1795706077233 — cùng một sự kiện (selector của switch), một khẳng định một phủ định; đề xuất gộp thành một thẻ bullet và xoá thẻ phủ định. Chờ quyết định.
- 1795750484756 "What does break do versus continue?" và 1795745004671 "What is the difference between break and continue?" — trùng nghĩa, giữ một.

### Subagent review — 3 cards flagged during example backfill (2026-11-28)

- `jv-0005-7f66c8a982` "When does findFirst() have to process every element?" — **giữ nguyên**. Subagent nghi ngờ, nhưng thẻ đúng: với stream rỗng, findFirst() phải đi hết pipeline để chứng minh không có phần tử, rồi trả Optional.empty().
- `jv-0005-5e8579bbb8` "What breaks when you fill a list with stream.forEach(result::add)?" — **sửa Back**. Back cũ nói side effect "blocks parallel execution" (sai: nó không chặn chạy song song, nó làm kết quả không an toàn/không xác định). Back mới: capturing an external mutable list makes the result unsafe because ArrayList cannot take concurrent writes. Front giữ nguyên nên CardKey không đổi.
- `jv-0005-5387bbeafb` "Which two arguments does Stream.max() ... require?" — **chờ quyết định**. Đáp án "Only a Comparator" là đúng; chính câu hỏi hỏi "two arguments" là sai. Sửa Front sẽ đổi CardKey (thẻ mới + xoá thẻ cũ), nên không tự làm.

### Subagent slice 3 review (2026-11-28)

- `jv-0004-3bfad91bdd` "Can a generic class extend Throwable?" — **sửa Back**. Cụm "not even as a type parameter" sai/độ mơ hồ: Java cấm generic class extend Throwable (trực tiếp hoặc gián tiếp), nhưng biến type được phép trong mệnh đề `throws` (`<T extends Exception> void m() throws T`). Front giữ nguyên, CardKey không đổi.

### Parallel subagents wave 2 (2026-11-28) — review

- `jv-0002-e8fd542fad` "What does a lambda class getSimpleName() return?" — **chờ sửa**. Back cũ "the name of the enclosing class" không đúng trên JDK 21: `Enclosing$$Lambda/0x...`. File `devjava-CHUNK-1.json` đang bị agent khác ghi, nên chưa sửa trong repo; sửa khi rảnh slot.
- `jv-0003-be5e17e4b9` "What must directly follow a try block's closing brace?" — **chờ sửa**. Back "A catch block — no code in between" quá chặt: `try { } finally { }` hợp lệ, và try-with-resources có thể đứng một mình. Cùng file đang bận.
- `jv-70-a722b3e393` "Can a switch match a range like >= 90?" — **chờ quyết định**. Back "No — case labels must be compile-time constants" đúng với switch cổ điển nhưng lỗi thời với Java 21: `case Integer i when i >= 90 ->` biên dịch được (subagent đã javac-verify). Sửa Back cần đánh giá lại cả thẻ.
- `jv-0007-*` (40 thẻ regex) — agent ghi ví dụ vào `devjava-CHUNK-4.json` nhưng file có deck string cũ `00 Java Roadmap::12 Documentation::03 Certifications and Validation` nên push.py từ chối. Đã ghi thẳng 40 field Example vào Anki theo CardKey, 40/40 readback OK; repo đã có nội dung từ commit 3e886c2.
- `jv-70-4214ce9f30`, `jv-70-2c12c0b771` — note không còn trong collection và không có entry trong repo; bỏ qua, không tạo lại.

### Subagents wave 3 (2026-11-28) — review

Đã sửa 9 Back (front giữ nguyên, CardKey không đổi): `Predicate.not`, `takeWhile/dropWhile` trên stream unordered, `UnaryOperator` vs `BinaryOperator`, `Consumer` vs `BiConsumer`, key HashMap bị mutate, wildcard subtyping, case label Java 21, 24 bytes Node vs 56 bytes LinkedList, và câu lỗi javac của lambda.

- `jv-0005-7778ca8d88` "Which three language constructs support pattern matching?" — **chờ quyết định**. Back says extended for loop, nhưng record patterns trong header của enhanced-for là preview ở Java 20 và bị gỡ ở Java 21. Sửa Back thành 2 constructs thì mâu thuẫn với chữ "three" trong Front; muốn đúng phải đổi Front (đổi CardKey) hoặc đổi số đếm.
- `jv-0004-eacb35c7a5`, `jv-0004-e93611d03c`, `jv-0004-09b4f6ed79`, `jv-0005-fc811726eb` — nuance nhỏ (Iterable cần iterator(), contains() có thể CCE runtime, Map.entry là snapshot, method reference overloading theo context). Giữ nguyên.
- `jv-0003-06d6fbf020` — source link `https://dev.java/organizing/jlink/` trả 404; nội dung đúng, chờ thay URL.

### Subagents wave 4 (2026-11-28) — review

Đã sửa 7 Back: charset overload của Files.lines(), IntStream.iterate không predicate, String.chars() trả UTF-16 code units (không phải code points), bốn factory lấy stream từ dữ liệu có sẵn, StreamSupport.stream chỉ nhận 2 đối số, pooling virtual threads, và greedy integrator không tự short-circuit. Audit cũng sửa 1 Example có `<br>&nbsp;` thay vì `<pre>` trần (note 1795706077218).

- `jv-0005-562a6d54b4` — Front hỏi characteristic được giữ lại nhưng Back nói SORTED/DISTINCT bị mất trên map/flatMap; câu hỏi sai, cần đổi Front (đổi CardKey). Chờ quyết định.
- `jv-0005-489470c1ac` — Back đúng (returned stream có thể parallel, Downstream không thread-safe), nhưng Front nói "@SafeVarargs-style care" — sai thuật ngữ. Chờ quyết định vì phải đổi Front.
- Gatherer cards (`jv-0005-388c2be329`, `jv-0005-1e3df302c9`, `jv-0005-23bf13f8c0`, `jv-0005-29cca3b976`, `jv-0005-307391e368`, `jv-0005-d55daef255`, `jv-0005-ea4832a5e6`, `jv-0005-ed50b9a640`, `jv-0005-fe983edd71`) — API JDK 24, javac máy đang là 21 nên snippet đánh dấu skip_javac; ví dụ dùng stand-in JDK 21 để minh hoạ cùng ngữ nghĩa.
- 11 assignment keys của slice 20 và 8 của slice 21 không còn khớp repo sau khi các card được re-key sang front plain-text; subagent đã verify 40/40 live note theo note ID, không trùng lặp.

### Subagents wave 5 (2026-11-28) — review

Đã sửa 3 Back: `exists()` là phương thức trả true khi file đã tồn tại (`createNewFile()` thì tạo file), JFR event streaming từ JDK 14 (JEP 349) không phải 16, và property đầy đủ là `com.sun.jndi.ldap.object.trustSerialData`.

- FFM/JDK 22+ (`java.lang.foreign`): 12 + 6 + 8 snippet đánh dấu skip_javac vì javac máy là 21.0.13 (API mới chỉ preview hoặc final ở 22); phần lớn đã syntax-check với `--enable-preview`. Không phải lỗi thẻ.
- `jv-0007-356cec563c` — chữ "required" cho StandardOpenOption.READ hơi lỏng (Extra nói mặc định là READ). Giữ nguyên.
- `jv-0007-4de0dae7f0` — card thu hẹp IV variance về block đầu; nguồn nói chung cho cả chuỗi block. Giữ nguyên.
- `jv-0007-f912e33161` — "hash encrypted with sender's private key" là cách nói rút gọn của nguồn; về mặt kỹ thuật là signing, không phải encryption. Chờ quyết định vì liên quan cả Front/Back.

### Subagents wave 6 (2026-11-28) — review

Đã sửa 2 Back trong `devjava-CHUNK-4.json` và ghi thẳng vào Anki vì file có deck string cũ `::03 Certifications and Validation` (live là `::02`): `.` không khớp line terminator trừ khi dùng DOTALL; ký tự đặc biệt trong replacement là backslash, `$` là group reference.

- 120 ví dụ từ map-agent-31/33/34 không lên được Anki vì cùng lý do deck cũ trong `devjava-CHUNK-4.json`; đã ghi trực tiếp theo CardKey, 120/120 note tồn tại, repo đã có nội dung.
- `devjava-CHUNK-4.json` cần renumber batch deck `::03` → `::02` để push.py không phải bỏ qua cả file nữa (việc riêng, không làm trong luồng ví dụ).
- `jv-0007-a6ffcbe4b4` — Front trình bày `Period.P10D` như một constant; không tồn tại. Back P10D đúng (từ `Period.ofDays(10)`). Sửa Front → đổi CardKey, chờ quyết định.
- `jv-0007-a367bd367b` ("Mobile java.time.zone" typo) và `jv-0007-9daa798345` (câu Extra bị cụt) — lỗi văn bản nhỏ, sự kiện đúng; chờ.
- `jv-0013-2b4b90209a`, `jv-0013-270a1c83aa`, `jv-0013-336be0e777` — Extra không liên quan đến Front/Back (bị dính từ thẻ khác). Cần audit riêng.
- Regex cards trích Boundaries page cho các sự kiện thực ra nằm ở Pattern/Quantifiers/Character Classes; nguồn chưa chính xác nhưng nội dung đúng.

### Deck migration + wave 7 (2026-11-28)

**Root cause đã sửa:** batch `00 Java Roadmap::12 Documentation::03 Certifications and Validation` trong `devjava-CHUNK-4.json` được đổi sang `::02` (tên deck đang sống). 8 note liên quan được đổi field CardKey theo key mới trước khi push để không tạo trùng; push trả 0 new / 0 updated / 243 unchanged, deck cũ biến mất, deck live có đúng 8 note. Từ giờ push.py không còn từ chối cả file này nữa.

Đã ghi 120 ví dụ của map-agent-36/37/38 vào Anki theo CardKey (repo đã có), sửa Back của `jv-0013-77a80adeb7` (`--inverse` phải đi với `--require`/`--package`/`--regex`), và đẩy commit 3cfa033.

- `jv-0013-5c38a75ca6` — default RSA 2048 của keytool phụ thuộc phiên bản (JDK 17: 2048, JDK 24/26 docs: 3072); thẻ cần ghi mốc JDK. Chờ.
- `jv-0013-2b4b90209a` — `kinit -password` không phải flag, password là đối số positional. Chờ vì phải đổi Front.
- Nhiều thẻ keytool/kinit/jar trích sai trang nguồn (jarsigner/jwebserver) nhưng nội dung đúng. Chờ dọn nguồn.
- 3 note jv-0013-aed7354487 / af4750f8f8 / b02a35219e đã có Example từ trước, không ghi đè.

### Subagents wave 8 (2026-11-28) — review

Đã sửa 4 Back: `-XX:MaxHeapFreeRatio=25` là 25% (không phải 0.25), `UseHugeTLBFS` tương đương `UseLargePages` và `UseSHM` là phương án Linux, `JFR.stop name=...` dùng name để chọn recording, và virtual threads không chữa StackOverflowError (vẫn có stack; dùng -Xss hoặc iterative).

- `jv-0013-fce39d5992` — Front nói `--startup file` "inherited startup disabled for that file"; dev.java nói `--startup` ghi đè script mặc định, còn `--no-startup` mới tắt và không dùng chung được. Chờ vì phải đổi Front.
- 40 ví dụ của slice 39–41 là command snippets (`skip_javac` đúng quy định); các lát trước đã có ví dụ Java biên dịch được.

### Subagents wave 9 (2026-11-28) — review

Đã làm rõ Back của `jv-0014-ae44c8b71d`: record đã tự sinh `toString()`, nhưng nên tự viết lại để ListView hiển thị đúng trường muốn thấy.

- `jv-0014-7793c55dc4` — Front viết "Compare-driven SortedList" (ý là comparator-driven); đáp án đúng. Chờ vì phải đổi Front.
- 40 ví dụ JavaFX/jpackage của slice 46 dùng `skip_javac` vì cần JavaFX runtime — đúng ngoại lệ CLI/jar.

### Subagents wave 10 (2026-11-28) — review

Đã sửa 4 Back: Evaluate Expression (tính/sửa biểu thức tại breakpoint, không phải "arbitrary Java"), overloading vs overriding (kể cả method kế thừa; overriding dispatch lúc chạy), `ArrayList.remove(int)` xóa theo chỉ số nên dùng `remove(Integer.valueOf(x))` để xóa theo giá trị, và private members được kế thừa nhưng không truy cập được.

- 120 ví dụ từ map-agent-50/51/52 đã ghi thẳng vào Anki theo CardKey vì 7 file sách `book-hfj3e-ch01..07.json` mang deck cũ, không có merge_into sống. Repo đã có nội dung.
- Cần migrate deck của các file sách HFJ3e sang deck roadmap đang sống (kèm đổi CardKey) để push.py không bỏ qua cả file nữa — TODO riêng, giống `devjava-CHUNK-4` trước đây.
- `jv-0015-9991a0d37a` — Java 25 compact source file, javac máy là 21 nên dùng snippet comment. `jv-0015-8986e0fa32` — pom.xml, đúng ngoại lệ skip_javac.

### Subagents wave 11 (2026-11-28) — review

Đã sửa 5 Back: `@Inherited` áp dụng cho annotation cấp class (method/field vẫn không kế thừa), bug compareTo là phép trừ tràn số (không phải dùng `<`), Java cho phép nhiều top-level class trong một file (ambiguity thật là định nghĩa trùng ở file khác), cleaner không resurrection được như finalizer, và default toString in `ClassName@<hex>` tùy máy.

- `jv-3003-e6ec171da9` trong `tij4e-ch03.json` không có note sống; push.py cố addNotes và bị reject do trùng. 9 thẻ được giao vẫn update tốt; thẻ này bỏ qua.
- `jv-4003-89800047d9` đã sửa; các ví dụ Effective Java Item 14/25/8/12 được javac-verify trước khi push.
