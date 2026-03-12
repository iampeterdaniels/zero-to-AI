import pytest

from src.io.fs import FS
from src.util.markdown import TextChunk, MarkdownChunker

# pytest -v tests/test_markdown.py


def collect_chunk_info(chunks: list[TextChunk]) -> dict:
    debug_dict = dict()
    chunk_list = list()
    for chunk_idx, chunk in enumerate(chunks):
        chunk_dict = dict()
        chunk_dict["chunk_idx"] = chunk_idx
        chunk_dict["line_count"] = chunk.line_count()
        chunk_dict["chunk_lines"] = chunk.lines
        chunk_list.append(chunk_dict)
    debug_dict["chunk_list"] = chunk_list
    return debug_dict


def test_text_chunk():
    chunk = TextChunk()
    chunk.add_line("This is a test.")
    chunk.add_line("This is only a test.")
    assert chunk.line_count() == 2
    assert not chunk.is_empty()
    assert chunk.as_text() == "This is a test.\nThis is only a test."


def test_empty_text_chunk():
    chunk = TextChunk()
    assert chunk.line_count() == 0
    assert chunk.is_empty()
    assert chunk.as_text() == ""


def test_simple_string_chunking():
    text = "Well, she was an American girl. Raised on promises."
    chunks = MarkdownChunker().chunk_content(text)
    assert len(chunks) == 1
    assert chunks[0].as_text() == text

    opts = dict()
    opts["chunk_strategy"] = "character_count"
    opts["max_chars_per_chunk"] = 40
    chunks = MarkdownChunker(opts=opts).chunk_content(text)
    assert len(chunks) == 2
    assert chunks[0].as_text() == "Well, she was an American girl."
    assert chunks[1].as_text() == "Raised on promises."


def test_chunking_us_constitution_by_page():
    # default options
    opts = dict()
    mc = MarkdownChunker(opts=opts)
    assert mc.chunk_strategy == "page"
    assert mc.max_chars_per_chunk == 8000

    # custom options
    opts = dict()
    opts["chunk_strategy"] = "pages"
    opts["max_chars_per_chunk"] = 7999
    mc = MarkdownChunker(opts=opts)
    assert mc.chunk_strategy == "pages"
    assert mc.max_chars_per_chunk == 7999

    content = FS.read("tests/fixtures/us_constitution.pdf.md")
    chunks = mc.chunk_content(content)
    debug_dict = collect_chunk_info(chunks)
    FS.write_json(debug_dict, "tmp/test_chunking_us_constitution_by_page.json")

    assert len(mc.content_lines) == 1552
    assert len(mc.errors) == 0
    assert len(chunks) == 19
    for chunk in chunks:
        assert isinstance(chunk, TextChunk)

    first_chunk = chunks[0]
    second_chunk = chunks[1]
    last_chunk = chunks[-1]

    assert first_chunk.line_count() == 7
    assert first_chunk.as_text().strip().startswith("# THE CONSTITUTION of the United States")
    assert first_chunk.as_text().strip().endswith("</figure>")

    assert second_chunk.line_count() == 84
    assert second_chunk.as_text().strip().startswith("# We the People of the United States")
    assert second_chunk.as_text().endswith(
        "the Legislature, which shall then fill such Vacancies.]*"
    )

    assert last_chunk.line_count() == 20
    assert "NATIONAL CONSTITUTION CENTER" in last_chunk.as_text()


def test_chunking_us_constitution_by_character_count():
    # custom options
    chunk_size = 2500
    opts = dict()
    opts["chunk_strategy"] = "character_count"
    opts["max_chars_per_chunk"] = chunk_size
    mc = MarkdownChunker(opts=opts)
    assert mc.chunk_strategy == "character_count"
    assert mc.max_chars_per_chunk == chunk_size

    content = FS.read("tests/fixtures/us_constitution.pdf.md")
    chunks = mc.chunk_content(content)
    debug_dict = collect_chunk_info(chunks)
    FS.write_json(debug_dict, "tmp/test_chunking_us_constitution_by_character_count.json")

    assert len(mc.content_lines) == 1552
    assert len(mc.errors) == 0
    assert len(chunks) == 23
    for chunk in chunks:
        assert isinstance(chunk, TextChunk)
        assert chunk.has_content() == True
        chunk_len = len(chunk.as_text())
        if chunk_len >= chunk_size:
            print("large chunk: {} {}".format(chunk_len, chunk.as_text()))
        assert chunk_len < chunk_size
