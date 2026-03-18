n8n main url: https://n8n.truehorizonai.com/webhook/

routes: /chatting [post]
request: {
    "id": 1,
    "chatInput": "input"
}

routes: /reportgen [get]
params: {
    "user_id": 1,
    "days": 14
}
