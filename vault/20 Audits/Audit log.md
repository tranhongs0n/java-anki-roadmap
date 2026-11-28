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
