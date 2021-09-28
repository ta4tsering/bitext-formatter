import re
from pathlib import Path
from uuid import uuid4
from openpecha.core.annotation import AnnBase, Span

from openpecha.core.pecha import OpenPechaFS
from openpecha.core.layer import Layer, LayerEnum

def get_unique_id():
    return uuid4().hex

def read_text(text_path):
    with open(text_path, encoding="utf8", errors='ignore') as f:
        contents = f.read()
    return contents

def get_segment_annotation(segment, char_walker):
    
    segment_annotation = {
        get_unique_id(): AnnBase(span=Span(start=char_walker, end=char_walker + len(segment) - 1))
    }
    return segment_annotation


def get_segment_layer(text):
    segment_annotations = {}
    char_walker = 0
    segments = text.splitlines()
    for segment in segments:
        if segment:
            segment_annotation  = get_segment_annotation(segment, char_walker)
            segment_annotations.update(segment_annotation)
        char_walker += len(segment)+1

    segment_layer = Layer(
        annotation_type = LayerEnum.segment,
        annotations = segment_annotations
    )
    return segment_layer


def create_opf(segmented_text_path, opf_path):
    opf = OpenPechaFS(opf_path=opf_path)
    segmented_text = read_text(segmented_text_path)
    layers = {
        'v001': {
            LayerEnum.segment: get_segment_layer(segmented_text)
        }  
    }
    bases = {
        'v001': segmented_text
    }
    opf.layers = layers
    opf.base = bases
    opf.save_base()
    opf.save_layers()

if __name__ == "__main__":
    chojok_paths = list(Path('./chojuk/segmented_text/').iterdir())
    chojok_paths.sort()
    for chojok_path in chojok_paths:
        chojok_text_paths = list(chojok_path.iterdir())
        for chojok_text_path in chojok_text_paths:
            text_id  = f'{chojok_path.stem}_{chojok_text_path.stem}'
            opf_path = f'./chojuk/opfs/{text_id}.opf/'
            create_opf(segmented_text_path= chojok_text_path, opf_path=opf_path)
            print(f'{text_id} completed..')