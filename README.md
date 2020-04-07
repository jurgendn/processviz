# THƯ VIỆN PROCESSVIZ - PROCESS VISUALIZATION

> Thư viện này được viết ra cho môn `Các mô hình ngẫu nhiên và ứng dụng`, sử dụng để mô tả Markov chain

## Dependencies

1. [networkx](https://networkx.github.io/)
2. [numpy](https://matplotlib.org/)
3. [matplotlib](https://numpy.org/)
4. [pandas](https://pandas.pydata.org/)

## Usage

Simple usage:

```python
import processviz as pvz

g = pvz.MarkovChain()
g.from_stdin(state=[1,2], data=[[0.8,0.2],[0.3,0.7]])
g.generate_graph()
```

This will generate a graph below:

### Instruction

To import library, use:

```python
import processviz as pvz
```

#### Table of Attribute

| attribute name          | use                                                          | syntax                                                       |
| ----------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| MarkovChain             | generate a empty Markov chain                                | processviz.MarkovChain()                                     |
| from_stdin              | import data to Markov chain manually                         | processviz.from_stdin(state = [(default None)], data = [default None], pi = [default None]) |
| from_file               | import data to Markov chain from file                        | processviz.from_file(path = 'matrix_input.csv')              |
| generate_state_graph    | visualize state graph through time                           | processviz.generate_state_graph(n = 1)                       |
| generate_graph          | generate process matrix at special step                      | processviz.generate_graph(n = 1)                             |
| has_path                | check if state j can be reached from state i                 | processviz.has_path(source, target)                          |
| is_connected            | check if two state is related                                | processviz.is_connected(source, target)                      |
| get_period              | get period of a state                                        | processviz.get_period(node)                                  |
| get_communicating_class | classify state into communicating sets                       | processviz.get_communicating_class()                         |
| is_regular              | check if a matrix is regular                                 | processviz.is_regular()                                      |
| is_irreducible          | chech if chain is irreducible or not                         | processviz.is_irreducible()                                  |
| get_mean_time           | return mean time spent to reach a set of states from a state | processviz.get_mean_time(source=None, target=None, type=['absoring', 'transient']) |
| is_recurrent            | check if a state is recurrent of transient                   | processviz.is_recurrent(state=None)                          |

### Example

_Example 1_: At a arbitrary time, there are 3 supermarkets with proportion [0.2,0.5,0.3] respectively.

Also we have a matrix [[0.8,0.1,0.1],[0.07,0.9,0.03],[0.083,0.067,0.85]]. In the future, what is the proportion of each supermarket

```python
import processviz as pvz

G = pvz.MarkovChain()
G.from_stdin(state = ['A', 'B', 'C'], data = [[0.8,0.1,0.1],[0.07,0.9,0.03],[0.083,0.067,0.85]], pi = [0.2,0.5,0.3])

'''
Visualize Markov chain and relationships in network
>>> G.generate_graph()
>>> Graph

Generate graph at a specific time
>>> G.generate_graph(time)
>>> Graph

Visualize distribution vector after k steps
>>> G.generate_state_graph(k)
>>> State_graph

Check if graph has a path to reach 'B' from 'A'
>>> G.is_connected('A', 'B')
>>> True

Check if matrix is regular
>>> G.is_regular()
>>> True

Get period of state 'i'
G.get_period(i)
>>> G.get_priod('A')
>>> 1

Get communicating class of state
G.get_connected_component()
>>> G.get_connected_component()
>>> [['A', 'B', 'C']]


Get mean time to reach a set of state from a particular state
G.get_mean_time(source='', target='', type='')
- Get mean time to get absoring state
>>> G.get_mean_time(type='absoring')
>>> 'No absoring state'
- Get mean time to reach state A from state B
>>> G.get_mean_time(source='B', target='A', type='transient')
>>> {fill later}
- Get mean time to reach state A from all state
>>> G.get_mean_time(target='A')
>>> []
- Get mean time to reach other states from state 'A'
>>>G.get_mean_time(source='A')
>>> []

Check a state is transient or recurrent
>>> G.is_recurrent(state='')
>>> True
```
#### Input from data file

To import from data file, please create a `csv` file, for example, by default, data is defined in `input.csv`:

```python
G.from_file(path)
```

Data file:

    - The first line is states, from left to right:
        * state1, state2,...
    - The second line is origin state vector:
        * 0.1, 0.2,....
    - From the third line, please fill in a square matrix, corresponding to matrix

---

## Note đối với môn học

Chi tiết về thi giữa kì và cuối kì, xem [tại đây](docs/Remark.md)
