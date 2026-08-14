import requests

url = 'https://cdnbbsr.s3waas.gov.in/s313111c20aee51aeb480ecbd988cd8cc9/uploads/2026/06/20260601632081678.pdf'
try:
    r = requests.get(url, timeout=20, headers={'User-Agent':'Mozilla/5.0'})
    print('status_code:', r.status_code)
    print('content-type:', r.headers.get('Content-Type'))
    print('content-length header:', r.headers.get('Content-Length'))
    print('first_bytes_len:', len(r.content[:512]))
    print('first_bytes_preview:', r.content[:64])
except Exception as e:
    print('ERROR', e)
