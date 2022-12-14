import flask

from apps.services.data_service import DataSvc


class _ViewMixin:
    def __init__(self):
        self.request = flask.request
        self.is_htmx_request = 'HX-Request' in flask.request.headers
        self.data_service = DataSvc()

    @property
    def segment(self):
        segment = self.request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    @property
    def window(self):
        # Just going to force lookback to be max 10 years since unadjusted data
        return self.request.form.get('window', '10Y')
