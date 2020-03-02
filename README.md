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
