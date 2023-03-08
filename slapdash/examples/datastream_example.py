import slapdash
import math
import random

@slapdash.refresh('graph', 0.5)
@slapdash.refresh('double_graph', 0.5)
class DatastreamDashboard:
    '''This model demonstrates the metadata decorator and the `isDataStream` property,
    which causes the property to be rendered as a line series.'''

    # supply data of the form (xs, ys), where xs and ys have the same length
    @property
    @slapdash.metadata({'renderAs': 'graph', 'units': ['x', 'y']})
    def graph(self):
        return list(range(100)), [10.*math.sin(i/(2*math.pi))+random.random() for i in range(100)]

    # supply data of the form ((xs1, ys1), (xs2, ys2), ...),
    # where len(xs1) = len(ys1), and so on.
    @property
    @slapdash.metadata({'renderAs': 'graph', 'units': ['x2', 'y2']})
    def double_graph(self):
        return (list(range(100)), [12.*math.sin(i/(2*math.pi))+random.random() for i in range(100)]),\
           (list(range(88)), [8.*math.sin(i/(2*math.pi))+random.random() for i in range(88)])


if __name__ == '__main__':
    slapdash.run(DatastreamDashboard())
