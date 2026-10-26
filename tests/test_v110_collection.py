"""Collection preserves partial native evidence without inventing completion."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('v110_partial_collection', ROOT/'docs/evaluation/coco-1.1.0/implementation/collect.py')
collect = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(collect)


class V110Collection(unittest.TestCase):
    def test_raw_completed_message_does_not_invent_missing_process_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); record = root/'record'; target = root/'packet'; record.mkdir(); target.mkdir()
            events = [{'type':'thread.started','thread_id':'example'},
                      {'type':'item.completed','item':{'type':'agent_message','text':'Actual emitted final.'}},
                      {'type':'turn.completed','usage':{'input_tokens':3,'output_tokens':2}}]
            (record/'turn-1.events.jsonl').write_text('\n'.join(json.dumps(e) for e in events)+'\n')
            metadata = {'state':'running','exit':None,'seconds':None}
            collect.write_turn(record,target,1,metadata)
            status = json.loads((target/'worker-1-status.json').read_text())
            self.assertTrue(status['raw_turn_completed'])
            self.assertIsNone(status['original_exit'])
            self.assertEqual(status['original_metadata_state'],'running')
            self.assertEqual((target/'worker-1-final.md').read_text(),'Actual emitted final.')
            self.assertEqual(metadata,{'state':'running','exit':None,'seconds':None})

    def test_interrupted_commentary_is_provisional_not_a_final_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);record=root/'record';target=root/'packet';record.mkdir();target.mkdir()
            event={'type':'item.completed','item':{'type':'agent_message','text':'I will repair it.'}}
            (record/'turn-1.events.jsonl').write_text(json.dumps(event)+'\n')
            collect.write_turn(record,target,1,{'state':'timed_out','exit':1,'seconds':420})
            self.assertFalse((target/'worker-1-final.md').exists())
            self.assertEqual((target/'worker-1-provisional.md').read_text(),'I will repair it.')

    def test_unstarted_queue_item_is_not_an_actor_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);record=root/'record';record.mkdir();target=root/'packet'
            collect.packet_trial({'record':str(record),'kind':'primary','seed':0},target)
            context=json.loads((target/'context.json').read_text())
            self.assertEqual(context['execution_state'],'not_attempted')
            self.assertIn('no actor was launched',context['unavailable'])
            self.assertEqual(json.loads((target/'public-outcomes.json').read_text()),{})
            self.assertEqual(list(target.glob('worker-*')),[])


if __name__=='__main__':unittest.main()
