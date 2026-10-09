#!/usr/bin/env python3
"""One bounded TypeSafe Jev call; store typed, reproducible avatar cue choices.

Uses the existing TypeSafe 1Password item privately. It does not copy Sean's code,
generate the avatar/audio, purchase credits, retry an uncertain POST, or provide
live Q&A. Run without --execute to stage/review the request without an API call.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import itertools
import json
import os
from pathlib import Path
import subprocess
import time
import urllib.error
import urllib.request

PROJECT = Path(__file__).resolve().parents[1]
OUTPUT = Path('/path/to/local-assets')
ENDPOINT = 'https://api.typesafe.ai/v1/systemone'
PRICE_PER_MILLION_INPUT = 0.042
# Provider docs impose at most 64k input tokens per request; output is free.
MAX_REQUEST_COST_USD = 65536 * PRICE_PER_MILLION_INPUT / 1_000_000
TASK_BUDGET_USD = 0.01

GESTURES = {
    'open_explain': 'Open-hand introduction or general explanation to the audience.',
    'write_board': 'Draw or trace lines on the transparent board to explain a diagram.',
    'point_timeline': 'Point along timeline dots to explain voice and motion timing.',
    'pull_to_space': 'Lift a diagram off the board into a spatial 3D arrangement.',
    'point_nodes': 'Point at specific connected voice/gesture/space nodes.',
    'closing': 'Bring the gesture to a calm closing position while summarizing.',
}
FOCUS = {
    'voice': 'The spoken explanation and its audio timing.',
    'gesture': 'The avatar hand movement and pointing/writing actions.',
    'space': 'The diagram becoming a spatial 3D object or spatial understanding.',
}
COLORS = {
    'teal': 'Teal emphasizes a voice/audio or explanatory sequence.',
    'lilac': 'Lilac emphasizes avatar motion and hand interaction.',
    'amber': 'Amber emphasizes spatial diagrams or a warm concluding insight.',
}
ORDERS = {
    '_'.join(order): 'Show the connected nodes in this order: ' + ', then '.join(order)
    for order in itertools.permutations(FOCUS)
}
ENGLISH = {
    'S01': 'This is a demo of my 3D avatar explaining in space.',
    'S02': 'Draw diagrams on a transparent board matched to what is being said.',
    'S03': 'First connect the voice and movement on one timeline.',
    'S04': 'These dots mark spoken timing; hand movements and lines advance together.',
    'S05': 'Next pull the diagram off the board and show it in three dimensions.',
    'S06': 'Words, gestures, spatial diagrams: one meaning conveyed in three ways.',
    'S07': 'Currently this replays a prepared explanation; question-driven generation is a future step.',
    'S08': 'See, hear, understand in space: this is a form of explanation.',
}


def dump(path: Path, value: object) -> None:
    staging = path.with_name(path.stem + '-staging' + path.suffix)
    staging.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    os.replace(staging, path)


def payload(story: dict) -> dict:
    state = {
        'demo': 'Ryo 160000-Gaussian body, authored IK gestures and scripted Japanese narration.',
        'task': 'Select visual/gesture orchestration from the closed allowed catalogs. This is an API-planned prerecorded demo, not live AI conversation.',
        'segments': [
            {'segment_id': s['id'], 'narration_ja': s['narration'], 'meaning_en': ENGLISH[s['id']]}
            for s in story['segments']
        ],
        'nodes': FOCUS,
    }
    questions = {}
    for segment in story['segments']:
        sid = segment['id']
        for field, criteria, decision in [
            ('gesture', GESTURES, 'Choose the hand gesture that best makes the narration understandable.'),
            ('focus_node', FOCUS, 'Choose which connected node should receive the most visible emphasis.'),
            ('emphasis_color', COLORS, 'Choose the emphasis color whose meaning best matches the narration.'),
            ('node_order', ORDERS, 'Choose a logical presentation order for the connected nodes based on this narration. Keep all three nodes.'),
        ]:
            questions[f'{sid}_{field}'] = {
                'type': 'choice',
                'instructions': f"For segment {sid} in `segments`, {decision} Base the choice on this segment's meaning, not a fixed position or numeric ID.",
                'criteria': criteria,
            }
    return {'model': 'jev-latest', 'state': state, 'questions': questions}


def private_key() -> str:
    return os.environ['TYPESAFE_API_KEY']


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--account-receipt', type=Path)
    args = parser.parse_args()
    story_bytes = (PROJECT / 'story.json').read_bytes()
    story = json.loads(story_bytes)
    request = payload(story)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    request_path = OUTPUT / 'jev-request.json'
    if not request_path.exists():
        dump(request_path, request)
    elif json.loads(request_path.read_text()) != request:
        raise RuntimeError('Preserving a preexisting request for a different story; review before replacing.')
    if not args.execute:
        print(json.dumps({'staged': str(request_path), 'questions': len(request['questions']), 'max_request_cost_usd': MAX_REQUEST_COST_USD}))
        return
    if not args.account_receipt:
        raise RuntimeError('Verified official-console account/balance receipt required.')
    account = json.loads(args.account_receipt.read_text())
    if account.get('provider') != 'TypeSafe AI' or account.get('console_host') != 'console.typesafe.ai':
        raise RuntimeError('Wrong provider/account receipt; no API call made.')
    if account.get('name') != 'Ryo Suzuki' or account.get('google_account') != 'ryosuzk@gmail.com':
        raise RuntimeError('Unexpected account; no API call made.')
    available = float(account['balance_usd'])
    if available < MAX_REQUEST_COST_USD or MAX_REQUEST_COST_USD > TASK_BUDGET_USD:
        raise RuntimeError('Insufficient existing-credit/task budget; no API call made.')
    started_path = OUTPUT / 'jev-call-started.json'
    if started_path.exists():
        raise RuntimeError('A POST was already started; reconcile its receipt before any explicit retry.')
    key = private_key()
    # Read-only authentication check. Do not log response headers or credentials.
    models_req = urllib.request.Request('https://api.typesafe.ai/v1/models', headers={'Authorization': 'Bearer ' + key})
    with urllib.request.urlopen(models_req, timeout=30) as response:
        models = json.loads(response.read())
    dump(OUTPUT / 'jev-models.json', models)
    if not any(x.get('name') == 'jev-latest' for x in models.get('models', [])):
        raise RuntimeError('Exact Jev alias not available to this account; no billable call made.')
    started = datetime.now(timezone.utc).isoformat()
    dump(started_path, {'started_at': started, 'endpoint': ENDPOINT, 'attempts': 1,
                        'max_charge_usd': MAX_REQUEST_COST_USD, 'existing_credit_before_usd': available})
    body = json.dumps(request, ensure_ascii=False).encode()
    req = urllib.request.Request(ENDPOINT, data=body,
                                 headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'}, method='POST')
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            raw = response.read().decode()
            http_status = response.status
            request_id = response.headers.get('x-request-id') or response.headers.get('request-id')
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode().replace(key, '[redacted]')
        dump(OUTPUT / 'jev-api-error.json', {'http_status': exc.code, 'body': raw, 'retry_performed': False})
        raise RuntimeError(f'TypeSafe returned HTTP {exc.code}; preserved error, no automatic retry.') from None
    except (TimeoutError, urllib.error.URLError):
        dump(OUTPUT / 'jev-api-error.json', {'error': 'transport_uncertain', 'retry_performed': False})
        raise RuntimeError('Transport result uncertain; do not retry before account reconciliation.') from None
    result = json.loads(raw.replace(key, '[redacted]'))
    dump(OUTPUT / 'jev-response.json', result)
    answers = result['answers']
    beats = []
    for s in story['segments']:
        sid = s['id']
        selected = {}
        confidence = {}
        for field, catalog in [('gesture', GESTURES), ('focus_node', FOCUS), ('emphasis_color', COLORS), ('node_order', ORDERS)]:
            answer = answers[f'{sid}_{field}']
            if answer.get('type') != 'choice' or answer.get('choice') not in catalog:
                raise RuntimeError(f'Invalid typed API answer for {sid}/{field}; raw response preserved.')
            selected[field] = answer['choice']
            confidence[field] = answer.get('confidence')
        selected['node_order'] = selected['node_order'].split('_')
        beats.append({'segment_id': sid, 'start': s['start'], 'end': s['end'], **selected,
                      'confidence': confidence, 'source_answer_ids': [f'{sid}_{f}' for f in ['gesture', 'focus_node', 'emphasis_color', 'node_order']]})
    usage = result.get('usage', {})
    estimated_charge = usage.get('input_tokens', 0) * PRICE_PER_MILLION_INPUT / 1_000_000
    proof = {'provider': 'TypeSafe AI', 'endpoint': ENDPOINT, 'requested_model': 'jev-latest',
             'actual_model': result['model'], 'http_status': http_status, 'request_id': request_id,
             'started_at': started, 'finished_at': datetime.now(timezone.utc).isoformat(),
             'elapsed_ms': round((time.perf_counter() - t0) * 1000, 2), 'usage': usage,
             'estimated_input_charge_usd': estimated_charge, 'price_per_million_input_usd': PRICE_PER_MILLION_INPUT,
             'pricing_source': 'https://docs.typesafe.ai/models', 'balance_before_usd': available,
             'actual_billing_observation': 'pending official console readback', 'attempts': 1,
             'credential_storage': '1Password Personal/TypeSafe Jev API key — Ryo avatar explainer/credential',
             'story_sha256': hashlib.sha256(story_bytes).hexdigest(), 'sean_source_reused': False}
    plan = {'schema': 'avatar-explainer-jev-plan.v1', 'mode': 'real-api-choices-recorded-for-replay',
            'boundary': 'Prerecorded scripted narration, actual Jev selected gesture/focus/color/order choices; no live AI Q&A or cloned voice.',
            'proof': proof, 'beats': beats}
    dump(OUTPUT / 'jev-plan.json', plan)
    dump(PROJECT / 'service' / 'plan.json', plan)
    dump(OUTPUT / 'jev-call-receipt.json', proof)
    print(json.dumps({'plan': str(OUTPUT / 'jev-plan.json'), 'actual_model': result['model'],
                      'usage': usage, 'estimated_charge_usd': estimated_charge, 'beats': len(beats),
                      'http_status': http_status, 'elapsed_ms': proof['elapsed_ms']}))


if __name__ == '__main__':
    main()
