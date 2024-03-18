"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file

Copyright 2023 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import qualtran.protos.annotations_pb2
import qualtran.protos.args_pb2
import qualtran.protos.ctrl_spec_pb2
import qualtran.protos.data_types_pb2
import qualtran.protos.registers_pb2
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class BloqArg(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    INT_VAL_FIELD_NUMBER: builtins.int
    FLOAT_VAL_FIELD_NUMBER: builtins.int
    STRING_VAL_FIELD_NUMBER: builtins.int
    SYMPY_EXPR_FIELD_NUMBER: builtins.int
    NDARRAY_FIELD_NUMBER: builtins.int
    REGISTER_FIELD_NUMBER: builtins.int
    SUBBLOQ_FIELD_NUMBER: builtins.int
    CIRQ_JSON_GZIP_FIELD_NUMBER: builtins.int
    QDATA_TYPE_FIELD_NUMBER: builtins.int
    CTRL_SPEC_FIELD_NUMBER: builtins.int
    name: builtins.str
    int_val: builtins.int
    float_val: builtins.float
    string_val: builtins.str
    sympy_expr: builtins.str
    """Sympy expression generated using str(expr)."""
    @property
    def ndarray(self) -> qualtran.protos.args_pb2.NDArray:
        """N-dimensional numpy array stored as bytes."""
    @property
    def register(self) -> qualtran.protos.registers_pb2.Register:
        """A Register object, accepted as an argument."""
    subbloq: builtins.int
    """Integer reference of a subbloq. Assumes access to a BloqLibrary."""
    cirq_json_gzip: builtins.bytes
    """Gzipped JSON corresponding to a Cirq object."""
    @property
    def qdata_type(self) -> qualtran.protos.data_types_pb2.QDataType:
        """data type"""
    @property
    def ctrl_spec(self) -> qualtran.protos.ctrl_spec_pb2.CtrlSpec:
        """Ctrl Spec for controlled bloqs"""
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        int_val: builtins.int = ...,
        float_val: builtins.float = ...,
        string_val: builtins.str = ...,
        sympy_expr: builtins.str = ...,
        ndarray: qualtran.protos.args_pb2.NDArray | None = ...,
        register: qualtran.protos.registers_pb2.Register | None = ...,
        subbloq: builtins.int = ...,
        cirq_json_gzip: builtins.bytes = ...,
        qdata_type: qualtran.protos.data_types_pb2.QDataType | None = ...,
        ctrl_spec: qualtran.protos.ctrl_spec_pb2.CtrlSpec | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["cirq_json_gzip", b"cirq_json_gzip", "ctrl_spec", b"ctrl_spec", "float_val", b"float_val", "int_val", b"int_val", "ndarray", b"ndarray", "qdata_type", b"qdata_type", "register", b"register", "string_val", b"string_val", "subbloq", b"subbloq", "sympy_expr", b"sympy_expr", "val", b"val"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["cirq_json_gzip", b"cirq_json_gzip", "ctrl_spec", b"ctrl_spec", "float_val", b"float_val", "int_val", b"int_val", "name", b"name", "ndarray", b"ndarray", "qdata_type", b"qdata_type", "register", b"register", "string_val", b"string_val", "subbloq", b"subbloq", "sympy_expr", b"sympy_expr", "val", b"val"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["val", b"val"]) -> typing_extensions.Literal["int_val", "float_val", "string_val", "sympy_expr", "ndarray", "register", "subbloq", "cirq_json_gzip", "qdata_type", "ctrl_spec"] | None: ...

global___BloqArg = BloqArg

@typing_extensions.final
class BloqLibrary(google.protobuf.message.Message):
    """A library of Bloqs. BloqLibrary should be used to represent both primitive Bloqs and
    composite Bloqs; i.e. Bloqs consisting of other subbloqs, like `CompositeBloq`,
    `ControlledBloq` etc.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class BloqWithDecomposition(google.protobuf.message.Message):
        """Decompositions are specified using integer IDs referencing other Bloqs within this library."""

        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        @typing_extensions.final
        class BloqCountsEntry(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor

            KEY_FIELD_NUMBER: builtins.int
            VALUE_FIELD_NUMBER: builtins.int
            key: builtins.int
            @property
            def value(self) -> qualtran.protos.args_pb2.IntOrSympy: ...
            def __init__(
                self,
                *,
                key: builtins.int = ...,
                value: qualtran.protos.args_pb2.IntOrSympy | None = ...,
            ) -> None: ...
            def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
            def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

        BLOQ_ID_FIELD_NUMBER: builtins.int
        DECOMPOSITION_FIELD_NUMBER: builtins.int
        BLOQ_COUNTS_FIELD_NUMBER: builtins.int
        BLOQ_FIELD_NUMBER: builtins.int
        bloq_id: builtins.int
        """Unique identifier for this Bloq within the library."""
        @property
        def decomposition(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Connection]:
            """Decomposition of the Bloq as an edge-list."""
        @property
        def bloq_counts(self) -> google.protobuf.internal.containers.MessageMap[builtins.int, qualtran.protos.args_pb2.IntOrSympy]:
            """Rough decomposition of the Bloq as bloq-counts."""
        @property
        def bloq(self) -> global___Bloq:
            """The Bloq itself."""
        def __init__(
            self,
            *,
            bloq_id: builtins.int = ...,
            decomposition: collections.abc.Iterable[global___Connection] | None = ...,
            bloq_counts: collections.abc.Mapping[builtins.int, qualtran.protos.args_pb2.IntOrSympy] | None = ...,
            bloq: global___Bloq | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["bloq", b"bloq"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["bloq", b"bloq", "bloq_counts", b"bloq_counts", "bloq_id", b"bloq_id", "decomposition", b"decomposition"]) -> None: ...

    NAME_FIELD_NUMBER: builtins.int
    TABLE_FIELD_NUMBER: builtins.int
    name: builtins.str
    """A name for the library."""
    @property
    def table(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___BloqLibrary.BloqWithDecomposition]: ...
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        table: collections.abc.Iterable[global___BloqLibrary.BloqWithDecomposition] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["name", b"name", "table", b"table"]) -> None: ...

global___BloqLibrary = BloqLibrary

@typing_extensions.final
class Bloq(google.protobuf.message.Message):
    """Messages to enable efficient description of a BloqLibrary, including Bloq decompositions in
    terms of other simpler bloqs.

    A Bloq without it's decomposition.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    ARGS_FIELD_NUMBER: builtins.int
    REGISTERS_FIELD_NUMBER: builtins.int
    T_COMPLEXITY_FIELD_NUMBER: builtins.int
    name: builtins.str
    """`name` identifies the Bloq."""
    @property
    def args(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___BloqArg]:
        """`Args` are used to construct the Bloq."""
    @property
    def registers(self) -> qualtran.protos.registers_pb2.Registers:
        """`Registers` specify the signature of the Bloq and are often derived using `args`."""
    @property
    def t_complexity(self) -> qualtran.protos.annotations_pb2.TComplexity:
        """Other useful annotations."""
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        args: collections.abc.Iterable[global___BloqArg] | None = ...,
        registers: qualtran.protos.registers_pb2.Registers | None = ...,
        t_complexity: qualtran.protos.annotations_pb2.TComplexity | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["registers", b"registers", "t_complexity", b"t_complexity"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["args", b"args", "name", b"name", "registers", b"registers", "t_complexity", b"t_complexity"]) -> None: ...

global___Bloq = Bloq

@typing_extensions.final
class BloqInstance(google.protobuf.message.Message):
    """Specific instance of a Bloq."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INSTANCE_ID_FIELD_NUMBER: builtins.int
    BLOQ_ID_FIELD_NUMBER: builtins.int
    instance_id: builtins.int
    bloq_id: builtins.int
    def __init__(
        self,
        *,
        instance_id: builtins.int = ...,
        bloq_id: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["bloq_id", b"bloq_id", "instance_id", b"instance_id"]) -> None: ...

global___BloqInstance = BloqInstance

@typing_extensions.final
class Soquet(google.protobuf.message.Message):
    """One half of a connection."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    BLOQ_INSTANCE_FIELD_NUMBER: builtins.int
    DANGLING_T_FIELD_NUMBER: builtins.int
    REGISTER_FIELD_NUMBER: builtins.int
    INDEX_FIELD_NUMBER: builtins.int
    @property
    def bloq_instance(self) -> global___BloqInstance: ...
    dangling_t: builtins.str
    @property
    def register(self) -> qualtran.protos.registers_pb2.Register: ...
    @property
    def index(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    def __init__(
        self,
        *,
        bloq_instance: global___BloqInstance | None = ...,
        dangling_t: builtins.str = ...,
        register: qualtran.protos.registers_pb2.Register | None = ...,
        index: collections.abc.Iterable[builtins.int] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["binst", b"binst", "bloq_instance", b"bloq_instance", "dangling_t", b"dangling_t", "register", b"register"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["binst", b"binst", "bloq_instance", b"bloq_instance", "dangling_t", b"dangling_t", "index", b"index", "register", b"register"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["binst", b"binst"]) -> typing_extensions.Literal["bloq_instance", "dangling_t"] | None: ...

global___Soquet = Soquet

@typing_extensions.final
class Connection(google.protobuf.message.Message):
    """A connection between two Soquets. Quantum compute graph can be represented as a list of
    connections.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LEFT_FIELD_NUMBER: builtins.int
    RIGHT_FIELD_NUMBER: builtins.int
    @property
    def left(self) -> global___Soquet: ...
    @property
    def right(self) -> global___Soquet: ...
    def __init__(
        self,
        *,
        left: global___Soquet | None = ...,
        right: global___Soquet | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["left", b"left", "right", b"right"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["left", b"left", "right", b"right"]) -> None: ...

global___Connection = Connection
