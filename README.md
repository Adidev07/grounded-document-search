# Grounded Document Search

Retrieve relevant passages from a tiny knowledge base with TF-IDF and return extractive answers with source citations.

AI-assisted learning project with synthetic data. No paid API, hosted model, or external dependency required.

## Run

Requires Python 3.10+.

```sh
python server.py
```

Open http://127.0.0.1:8000. Alternative port: `python server.py --port 8001`. On Windows, `py` can replace `python`. Stop with Ctrl+C.

## Test

```sh
python -m unittest discover -v
```

## Detailed documentation

Read [PROJECT_GUIDE.pdf](PROJECT_GUIDE.pdf) for architecture, file responsibilities, algorithms, API examples, limits, demo instructions, GitHub setup and interview preparation. The same guide is available as editable [GUIDE.md](GUIDE.md).

## Demo

Support teams need answers that can be traced to source documents. Search for refund, shipping or API keys and inspect the returned passage and source. Ask about volcanoes to see an explicit no-evidence result. This app returns existing text instead of generating an answer, so it is a transparent retrieval foundation for a future RAG assistant.

## Limits

Local single-process demo; no authentication. Use synthetic inputs. Do not expose the development server publicly. Rules and fixture-based metrics do not establish real model quality.

## Make it yours

Run it, inspect the code, replace fixtures with your own public examples and implement a documented improvement. Explain which parts were AI-assisted and what you changed.

## License

MIT; see LICENSE.
