# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag

from conduit.app import create_app
from conduit.settings import DevConfig, ProdConfig

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from grpc import ssl_channel_credentials
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# resource describes app-level information that will be added to all spans
resource = Resource(attributes={
    "service.name": "Honeycomb Interview"
})

# create new trace provider with our resource
trace_provider = TracerProvider(resource=resource)

# create exporter to send spans to Honeycomb
otlp_exporter = OTLPSpanExporter(
    endpoint="api.honeycomb.io:443",
    insecure=False,
    credentials=ssl_channel_credentials(),
    headers=(
        ("x-honeycomb-team", "8190a1aba6baa0a3c99759d88fc0ada6"),
        ("x-honeycomb-dataset", "traces"))
    )

# register exporter with provider
trace_provider.add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

# register trace provider
trace.set_tracer_provider(trace_provider)

CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)
FlaskInstrumentor().instrument_app(app)
