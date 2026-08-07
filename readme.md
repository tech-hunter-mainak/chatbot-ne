## Configuration of Backend
```
backend/
│
├── app/
│   │
│   ├── main.py                    # FastAPI entry point
│   ├── config.py                  # Environment variables & configuration
│   ├── dependencies.py            # Shared dependencies
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py              # API router
│   │   ├── chat.py                # Chat endpoint
│   │   ├── health.py              # Health check
│   │   └── knowledge.py           # Knowledge management endpoints
│   │
│   ├── models/
│   │   ├── request.py             # Request schemas
│   │   ├── response.py            # Response schemas
│   │   └── okf.py                 # OKF schema
│   │
│   ├── services/
│   │   ├── chat_service.py
│   │   ├── rag_service.py
│   │   ├── retrieval_service.py
│   │   ├── embedding_service.py
│   │   ├── llm_service.py
│   │   ├── reranker_service.py
│   │   ├── okf_loader.py
│   │   └── prompt_service.py
│   │
│   ├── vectorstore/
│   │   ├── faiss_manager.py
│   │   ├── index_builder.py
│   │   └── search.py
│   │
│   ├── preprocessing/
│   │   ├── text_cleaner.py
│   │   ├── chunking.py
│   │   └── metadata.py
│   │
│   ├── prompts/
│   │   ├── system_prompt.txt
│   │   ├── rag_prompt.txt
│   │   └── answer_prompt.txt
│   │
│   ├── utils/
│   │   ├── logger.py
│   │   ├── helpers.py
│   │   ├── constants.py
│   │   └── validators.py
│   │
│   └── database/
│       ├── vector_db/
│       └── cache/
│
├── knowledge/
│   │
│   ├── asm/
│   ├── kha/
│   ├── grt/
│   ├── lus/
│   ├── nag/
│   ├── trp/
│   ├── ccp/
│   └── wao/
│
├── scripts/
│   ├── ingest_okf.py
│   ├── build_embeddings.py
│   ├── rebuild_index.py
│   └── validate_okf.py
│
├── tests/
│   ├── test_api.py
│   ├── test_rag.py
│   ├── test_embeddings.py
│   └── test_okf.py
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```