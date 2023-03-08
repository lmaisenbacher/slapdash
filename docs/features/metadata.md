You can attach a set of metadata to your interface properties by defining them in a `_metadata` hidden attribute:

=== "interface"

    ```python
    class MetadataDashboard:
        float_prop: float = 0.35
        list_prop: List[float] = []
        image: str = ""

        _metadata = {
            'float_prop': {'min': 0, 'max': 10, 'step': 0.01, 'units': 'MHz'},
            'list_prop': {'units': 'kg', 'step': 0.1},
            'image': {'isImage': True},
        }
    ```

=== "web"

    image here

where the keys are the name of the properties you want to attach the metadata to, and the value is a metadata dictionary.

Metadata can be chosen among a set of few allowed ones defined by the specification below, and are mostly used to make a nicer web frontend. When the dashboard Model is built it performs a few sanity checks on the provided `_metadata`, in this order:

- metadata can only be assigned to a property that actually exists in the Model
- the metadata name must be allowed
- the type of the metadata value must be among the ones listed in _type_
- metadata must be assigned to a property whose type is among the ones listed in _prop_type_

Any exception to these rules will throw a warning and the corresponding entry is ignored and removed from the `_metadata` dictionary.

## Allowed metadata
