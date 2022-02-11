import sys
from werkzeug.middleware.dispatcher import DispatcherMiddleware # use to combine each Flask app into a larger one that is dispatched based on prefix

sys.path.insert(1, "/Users/giacomo/OneDrive - Universita' degli Studi dell'Aquila/Università/Magistrale/1º anno/Software Architectures/SA/microservices")

from microservices.Artworks_curator.app import app as artwork_curator
from microservices.Localizator.app import app as localizator
from microservices.middleware.app import app as middleware
from microservices.Visitors_validation.app import app as visitors_validation

from app import app
application = DispatcherMiddleware(app,{
    '/middleware':middleware,
    '/artwork_curator':artwork_curator,
    '/localizator':localizator,
    '/visitors_validation':visitors_validation
})

