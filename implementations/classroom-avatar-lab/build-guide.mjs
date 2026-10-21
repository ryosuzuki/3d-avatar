import fs from 'node:fs';
import {marked} from 'marked';
const body=marked.parse(fs.readFileSync(new URL('./GUIDE.md',import.meta.url),'utf8'));
fs.writeFileSync(new URL('./guide.html',import.meta.url),`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Unity & AR Guide · Avatar Lab</title><link rel="stylesheet" href="/style.css"></head><body><header><a class="brand" href="/">◈ <span>AVATAR LAB</span></a><nav><a href="/">← Back to studio</a></nav></header><main class="guide">${body}</main></body></html>`);
