#!/usr/bin/env python

# Copyright 2021 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to perform basic schema operations
using the Cloud Pub/Sub API.

For more information, see the README.md under /pubsub and the documentation
at https://cloud.google.com/pubsub/docs/schemas.
"""

import argparse


def create_avro_schema(project_id, schema_id, avsc_file):
    """Create a schema resource from a JSON-formatted Avro schema file."""
    # [START pubsub_create_avro_schema]
    from google.api_core.exceptions import AlreadyExists
    from google.cloud.pubsub import SchemaServiceClient
    from google.pubsub_v1.types import Schema

    # TODO(developer): Replace these variables before running the sample.
    # project_id = "your-project-id"
    # schema_id = "your-schema-id"
    # avsc_file = "path/to/an/avro/schema/file/(.avsc)/formatted/in/json"

    project_path = f"projects/{project_id}"

    # Read a JSON-formatted Avro schema file as a string.
    with open(avsc_file, "rb") as f:
        avsc_source = f.read().decode("utf-8")

    schema_client = SchemaServiceClient()
    schema_path = schema_client.schema_path(project_id, schema_id)
    schema = Schema(name=schema_path, type_=Schema.Type.AVRO, definition=avsc_source)

    try:
        result = schema_client.create_schema(
            request={"parent": project_path, "schema": schema, "schema_id": schema_id}
        )
        print(f"Created a schema using an Avro schema file:\n{result}")
    except AlreadyExists:
        print(f"{schema_id} already exists.")
    # [END pubsub_create_avro_schema]


def create_proto_schema(project_id, schema_id, proto_file):
    """Create a schema resource from a protobuf schema file."""
    # [START pubsub_create_proto_schema]
    from google.api_core.exceptions import AlreadyExists
    from google.cloud.pubsub import SchemaServiceClient
    from google.pubsub_v1.types import Schema

    # TODO(developer): Replace these variables before running the sample.
    # project_id = "your-project-id"
    # schema_id = "your-schema-id"
    # proto_file = "path/to/a/proto/file/(.proto)/formatted/in/protocol/buffers"

    project_path = f"projects/{project_id}"

    # Read a protobuf schema file as a string.
    with open(proto_file, "rb") as f:
        proto_source = f.read().decode("utf-8")

    schema_client = SchemaServiceClient()
    schema_path = schema_client.schema_path(project_id, schema_id)
    schema = Schema(
        name=schema_path, type_=Schema.Type.PROTOCOL_BUFFER, definition=proto_source
    )

    try:
        result = schema_client.create_schema(
            request={"parent": project_path, "schema": schema, "schema_id": schema_id}
        )
        print(f"Created a schema using a protobuf schema file:\n{result}")
    except AlreadyExists:
        print(f"{schema_id} already exists.")
    # [END pubsub_create_proto_schema]


def get_schema(project_id, schema_id):
    """Get a schema resource."""
    # [START pubsub_get_schema]
    from google.api_core.exceptions import NotFound
    from google.cloud.pubsub import SchemaServiceClient

    # TODO(developer): Replace these variables before running the sample.
    # project_id = "your-project-id"
    # schema_id = "your-schema-id"

    schema_client = SchemaServiceClient()
    schema_path = schema_client.schema_path(project_id, schema_id)

    try:
        result = schema_client.get_schema(request={"name": schema_path})
        print(f"Got a schema:\n{result}")
    except NotFound:
        print(f"{schema_id} not found.")
    # [END pubsub_get_schema]


def list_schemas(project_id):
    """List schema resources."""
    # [START pubsub_list_schemas]
    from google.cloud.pubsub import SchemaServiceClient

    # TODO(developer): Replace these variables before running the sample.
    # project_id = "your-project-id"

    project_path = f"projects/{project_id}"
    schema_client = SchemaServiceClient()

    for schema in schema_client.list_schemas(request={"parent": project_path}):
        print(schema)

    print("Listed schemas.")
    # [END pubsub_list_schemas]


def delete_schema(project_id, schema_id):
    """Delete a schema resource."""
    # [START pubsub_delete_schema]
    from google.api_core.exceptions import NotFound
    from google.cloud.pubsub import SchemaServiceClient

    # TODO(developer): Replace these variables before running the sample.
    # project_id = "your-project-id"
    # schema_id = "your-schema-id"

    schema_client = SchemaServiceClient()
    schema_path = schema_client.schema_path(project_id, schema_id)

    try:
        schema_client.delete_schema(request={"name": schema_path})
        print(f"Deleted a schema:\n{schema_path}")
    except NotFound:
        print(f"{schema_id} not found.")
    # [END pubsub_delete_schema]


def create_topic_with_schema(project_id, topic_id, schema_id, message_encoding):
    """Create a topic resource with a schema."""
    # [START pubsub_create_topic_with_schema]
    from google.api_core.exceptions import AlreadyExists, InvalidArgument
    from google.cloud.pubsub import PublisherClient, SchemaServiceClient
    from google.pubsub_v1.types import Encoding

    # TODO(developer): Replace these variables before running the sample.
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"
    # schema_id = "your-schema-id"
    # Choose either BINARY or JSON as valid message encoding in this topic.
    # message_encoding = "BINARY"

    publisher_client = PublisherClient()
    topic_path = publisher_client.topic_path(project_id, topic_id)

    schema_client = SchemaServiceClient()
    schema_path = schema_client.schema_path(project_id, schema_id)

    if message_encoding == "BINARY":
        encoding = Encoding.BINARY
    elif message_encoding == "JSON":
        encoding = Encoding.JSON
    else:
        encoding = Encoding.ENCODING_UNSPECIFIED

    try:
        response = publisher_client.create_topic(
            request={
                "name": topic_path,
                "schema_settings": {"schema": schema_path, "encoding": encoding},
            }
        )
        print(f"Created a topic:\n{response}")

    except AlreadyExists:
        print(f"{topic_id} already exists.")
    except InvalidArgument:
        print("Please choose either BINARY or JSON as a valid message encoding type.")
    # [END pubsub_create_topic_with_schema]


def publish_avro_records(project_id, topic_id, avsc_file):
    """Pulbish a BINARY or JSON encoded message to a topic configured with an Avro schema."""
    # [START pubsub_publish_avro_records]
    from avro.io import BinaryEncoder, DatumWriter
    import avro
    import io
    import json
    from google.api_core.exceptions import NotFound
    from google.cloud.pubsub import PublisherClient
    from google.pubsub_v1.types import Encoding

    # TODO(developer): Replace these variables before running the sample.
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"
    # avsc_file = "path/to/an/avro/schema/file/(.avsc)/formatted/in/json"

    publisher_client = PublisherClient()
    topic_path = publisher_client.topic_path(project_id, topic_id)

    # Prepare to write Avro records to the binary output stream.
    avro_schema = avro.schema.parse(open(avsc_file, "rb").read())
    writer = DatumWriter(avro_schema)
    bout = io.BytesIO()

    # Prepare some data using a Python dictionary that matches the Avro schema
    record = {"name": "Alaska", "post_abbr": "AK"}

    try:
        # Get the topic encoding type.
        topic = publisher_client.get_topic(request={"topic": topic_path})
        encoding = topic.schema_settings.encoding

        # Encode the data according to the message serialization type.
        if encoding == Encoding.BINARY:
            encoder = BinaryEncoder(bout)
            writer.write(record, encoder)
            data = bout.getvalue()
            print(f"Preparing a binary-encoded message:\n{data}")
        elif encoding == Encoding.JSON:
            data = json.dumps(record).encode("utf-8")
            print(f"Preparing a JSON-encoded message:\n{data}")
        else:
            print(f"No encoding specified in {topic_path}. Abort.")
            exit(0)

        future = publisher_client.publish(topic_path, data)
        print(f"Published message ID: {future.result()}")

    except NotFound:
        print(f"{topic_id} not found.")
    # [END pubsub_publish_avro_records]


def publish_proto_messages(project_id, topic_id):
    """Publish a BINARY or JSON encoded message to a topic configured with a protobuf schema."""
    # [START pubsub_publish_proto_messages]
    from google.api_core.exceptions import NotFound
    from google.cloud.pubsub import PublisherClient
    from google.protobuf.json_format import MessageToJson
    from google.pubsub_v1.types import Encoding

    from utilities import us_states_pb2

    # TODO(developer): Replace these variables before running the sample.
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"

    publisher_client = PublisherClient()
    topic_path = publisher_client.topic_path(project_id, topic_id)

    try:
        # Get the topic encoding type.
        topic = publisher_client.get_topic(request={"topic": topic_path})
        encoding = topic.schema_settings.encoding

        # Instantiate a protoc-generated class defined in `us-states.proto`.
        state = us_states_pb2.StateProto()
        state.name = "Alaska"
        state.post_abbr = "AK"

        # Encode the data according to the message serialization type.
        if encoding == Encoding.BINARY:
            data = state.SerializeToString()
            print(f"Preparing a binary-encoded message:\n{data}")
        elif encoding == Encoding.JSON:
            json_object = MessageToJson(state)
            data = str(json_object).encode("utf-8")
            print(f"Preparing a JSON-encoded message:\n{data}")
        else:
            print(f"No encoding specified in {topic_path}. Abort.")
            exit(0)

        future = publisher_client.publish(topic_path, data)
        print(f"Published message ID: {future.result()}")

    except NotFound:
        print(f"{topic_id} not found.")
    # [END pubsub_publish_proto_messages]


def subscribe_with_avro_schema(project_id, subscription_id, avsc_file, timeout=None):
    """Receive and decode messages sent to a topic with an Avro schema."""
    # [START pubsub_subscribe_avro_records]
    import avro
    from avro.io import BinaryDecoder, DatumReader
    from concurrent.futures import TimeoutError
    import io
    import json
    from google.cloud.pubsub import SubscriberClient

    # TODO(developer)
    # project_id = "your-project-id"
    # subscription_id = "your-subscription-id"
    # avsc_file = "path/to/an/avro/schema/file/(.avsc)/formatted/in/json"
    # Number of seconds the subscriber listens for messages
    # timeout = 5.0

    subscriber = SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    avro_schema = avro.schema.parse(open(avsc_file, "rb").read())

    def callback(message):
        # Get the message serialization type.
        encoding = message.attributes.get("googclient_schemaencoding")
        # Deserialize the message data accordingly.
        if encoding == "BINARY":
            bout = io.BytesIO(message.data)
            decoder = BinaryDecoder(bout)
            reader = DatumReader(avro_schema)
            message_data = reader.read(decoder)
            print(f"Received a binary-encoded message:\n{message_data}")
        elif encoding == "JSON":
            message_data = json.loads(message.data)
            print(f"Received a JSON-encoded message:\n{message_data}")
        else:
            print(f"Received a message with no encoding:\n{message}")

        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception occurs first.
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.
    # [END pubsub_subscribe_avro_records]


def subscribe_with_proto_schema(project_id, subscription_id, timeout):
    """Receive and decode messages sent to a topic with a protobuf schema."""
    # [[START pubsub_subscribe_proto_messages]
    from concurrent.futures import TimeoutError
    from google.cloud.pubsub import SubscriberClient
    from google.protobuf.json_format import Parse

    from utilities import us_states_pb2

    # TODO(developer)
    # project_id = "your-project-id"
    # subscription_id = "your-subscription-id"
    # Number of seconds the subscriber listens for messages
    # timeout = 5.0

    subscriber = SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    # Instantiate a protoc-generated class defined in `us-states.proto`.
    state = us_states_pb2.StateProto()

    def callback(message):
        # Get the message serialization type.
        encoding = message.attributes.get("googclient_schemaencoding")
        # Deserialize the message data accordingly.
        if encoding == "BINARY":
            state.ParseFromString(message.data)
            print("Received a binary-encoded message:\n{state}")
        elif encoding == "JSON":
            Parse(message.data, state)
            print(f"Received a JSON-encoded message:\n{state}")
        else:
            print(f"Received a message with no encoding:\n{message}")

        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception occurs first.
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()  # Trigger the shutdown.
            streaming_pull_future.result()  # Block until the shutdown is complete.
    # [END pubsub_subscribe_proto_messages]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="Your Google Cloud project ID")

    subparsers = parser.add_subparsers(dest="command")

    create_avro_schema_parser = subparsers.add_parser(
        "create-avro", help=create_avro_schema.__doc__
    )
    create_avro_schema_parser.add_argument("schema_id")
    create_avro_schema_parser.add_argument("avsc_file")

    create_proto_schema_parser = subparsers.add_parser(
        "create-proto", help=create_proto_schema.__doc__
    )
    create_proto_schema_parser.add_argument("schema_id")
    create_proto_schema_parser.add_argument("proto_file")

    get_schema_parser = subparsers.add_parser("get", help=get_schema.__doc__)
    get_schema_parser.add_argument("schema_id")

    list_schemas_parser = subparsers.add_parser("list", help=list_schemas.__doc__)

    delete_schema_parser = subparsers.add_parser("delete", help=delete_schema.__doc__)
    delete_schema_parser.add_argument("schema_id")

    create_topic_with_schema_parser = subparsers.add_parser(
        "create-topic", help=create_topic_with_schema.__doc__
    )
    create_topic_with_schema_parser.add_argument("topic_id")
    create_topic_with_schema_parser.add_argument("schema_id")
    create_topic_with_schema_parser.add_argument(
        "message_encoding", choices=["BINARY", "JSON"]
    )

    publish_avro_records_parser = subparsers.add_parser(
        "publish-avro", help=publish_avro_records.__doc__
    )
    publish_avro_records_parser.add_argument("topic_id")
    publish_avro_records_parser.add_argument("avsc_file")

    publish_proto_messages_parser = subparsers.add_parser(
        "publish-proto", help=publish_proto_messages.__doc__
    )
    publish_proto_messages_parser.add_argument("topic_id")

    subscribe_with_avro_schema_parser = subparsers.add_parser(
        "receive-avro", help=subscribe_with_avro_schema.__doc__
    )
    subscribe_with_avro_schema_parser.add_argument("subscription_id")
    subscribe_with_avro_schema_parser.add_argument("avsc_file")
    subscribe_with_avro_schema_parser.add_argument(
        "timeout", default=None, type=float, nargs="?"
    )

    subscribe_with_proto_schema_parser = subparsers.add_parser(
        "receive-proto", help=subscribe_with_proto_schema.__doc__
    )
    subscribe_with_proto_schema_parser.add_argument("subscription_id")
    subscribe_with_proto_schema_parser.add_argument(
        "timeout", default=None, type=float, nargs="?"
    )

    args = parser.parse_args()

    if args.command == "create-avro":
        create_avro_schema(args.project_id, args.schema_id, args.avsc_file)
    if args.command == "create-proto":
        create_proto_schema(args.project_id, args.schema_id, args.proto_file)
    if args.command == "get":
        get_schema(args.project_id, args.schema_id)
    if args.command == "list":
        list_schemas(args.project_id)
    if args.command == "delete":
        delete_schema(args.project_id, args.schema_id)
    if args.command == "create-topic":
        create_topic_with_schema(
            args.project_id, args.topic_id, args.schema_id, args.message_encoding
        )
    if args.command == "publish-avro":
        publish_avro_records(args.project_id, args.topic_id, args.avsc_file)
    if args.command == "publish-proto":
        publish_proto_messages(args.project_id, args.topic_id)
    if args.command == "receive-avro":
        subscribe_with_avro_schema(
            args.project_id, args.subscription_id, args.avsc_file, args.timeout
        )
    if args.command == "receive-proto":
        subscribe_with_proto_schema(args.project_id, args.subscription_id, args.timeout)
