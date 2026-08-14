import sys
from pathlib import Path

# Ensure repo root is on sys.path so `app` package imports work when running scripts
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.llm_service import llm_service


def main() -> None:
    try:
        out = llm_service.generate('আপোনালোকৰ জিলাত কোনটো উৎসৱ সুপ্ৰসিদ্ধ?', [], 'asm')
        print('---OUTPUT---')
        print(out)
    except Exception as e:
        print('ERROR:', e)


if __name__ == '__main__':
    main()
