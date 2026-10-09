// Independent renderer adapter, not Sean's code or a provider SDK implementation.
export const COLORS={teal:'#84efda',lilac:'#b6bff5',amber:'#f2c48d'};
export const NODE={voice:0,gesture:1,space:2};
export function validatePlan(plan){
 if(!plan||!Array.isArray(plan.beats)||!plan.beats.length)throw Error('Missing API-generated cue plan');
 const gestures=new Set(['open_explain','write_board','point_timeline','pull_to_space','point_nodes','closing']);
 for(const b of plan.beats){
  if(!/^S0[1-8]$/.test(b.segment_id)||!gestures.has(b.gesture))throw Error('Invalid segment / gesture in API cue plan');
  if(b.focus_node&&!Object.hasOwn(NODE,b.focus_node))throw Error('Invalid cue focus node');
  if(b.emphasis_color&&!Object.hasOwn(COLORS,b.emphasis_color))throw Error('Invalid cue emphasis color');
 }
 return plan;
}
export function cueFor(plan,segment){return plan.beats.find(b=>b.segment_id===segment)||null}
export function nodeFocus(beat,p){
 if(beat?.gesture==='point_nodes'&&Array.isArray(beat?.node_order)&&beat.node_order.length){const node=beat.node_order[Math.min(beat.node_order.length-1,Math.floor(p*beat.node_order.length))];return NODE[node]??0}
 return NODE[beat?.focus_node]??0;
}
