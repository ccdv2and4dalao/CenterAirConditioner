import contextvars
from contextlib import contextmanager


class AsyncContext(object):
    def __init__(self, context_ref, ref_name='_async_context', ref_fac_name=None):
        self.ref_name = ref_name
        self.ref_fac_name = ref_fac_name or ref_name + '_fac'
        setattr(self, self.ref_name, contextvars.ContextVar(ref_name, default=context_ref()))
        setattr(self, self.ref_fac_name, context_ref)

    @contextmanager
    def async_context(self):
        getattr(self, self.ref_name).set(getattr(self, self.ref_fac_name)())
        yield self
