import time
import random
import matplotlib.pyplot as plt
import networkx as nx
from tqdm import tqdm


# Generate a random directed graph with capacities and weights
def generate_random_graph(n, density=0.01, max_capacity=100, max_weight=10):

    graph = nx.DiGraph()

    # Add nodes
    for i in range(n):
        graph.add_node(i)

    # Add edges with random capacities and weights
    for i in range(n):
        for j in range(n):
            if i != j and random.random() < density:
                capacity = random.randint(1, max_capacity)
                weight = random.randint(1, max_weight)
                graph.add_edge(i, j, capacity=capacity, weight=weight)

    return graph


# Measure execution time of a given algorithm
def measure_execution_time(algorithm, graph, source, sink):

    start_time = time.time()
    result = algorithm(graph, source, sink)
    elapsed_time = time.time() - start_time
    return elapsed_time, result


# Ford-Fulkerson algorithm
def ford_fulkerson_algorithm(graph, source, sink):
    return nx.maximum_flow(graph, source, sink, flow_func=nx.algorithms.flow.edmonds_karp)


# Push-Relabel algorithm
def push_relabel_algorithm(graph, source, sink):
    return nx.maximum_flow(graph, source, sink, flow_func=nx.algorithms.flow.preflow_push)


# Min-Cost Flow algorithm
def min_cost_flow_algorithm(graph, source, sink):
    for u, v, data in graph.edges(data=True):
        if "weight" not in data:
            data["weight"] = random.randint(1, 10)

    total_flow = sum(data["capacity"] for u, v, data in graph.edges(data=True) if u == source)
    graph.nodes[source]["demand"] = -total_flow
    graph.nodes[sink]["demand"] = total_flow

    for node in graph.nodes:
        if node != source and node != sink:
            graph.nodes[node]["demand"] = 0

    cost, flow_dict = nx.network_simplex(graph)
    return cost, flow_dict


# Analyze complexity of different algorithms
def analyze_complexity():
    """
    Run complexity analysis and collect results for multiple graph sizes.
    """
    results = {"test_number": [], "graph_size": [], "theta_FF": [], "theta_PR": [], "theta_MIN": []}
    n_values = [10, 20, 40, 100, 1000]
    test_count = 100  # Number of tests per size

    for n in n_values:
        print(f"Testing for graph size n = {n}...")

        for test_num in tqdm(range(1, test_count + 1), desc=f"Progress for n={n}", unit="test"):
            graph = generate_random_graph(n, density=0.01)
            source, sink = 0, n - 1

            theta_FF, _ = measure_execution_time(ford_fulkerson_algorithm, graph, source, sink)
            theta_PR, _ = measure_execution_time(push_relabel_algorithm, graph, source, sink)

            try:
                theta_MIN, _ = measure_execution_time(min_cost_flow_algorithm, graph, source, sink)
            except nx.NetworkXUnfeasible as e:
                print(f"Error in Min-Cost Flow: {e}")
                theta_MIN = None

            results["test_number"].append(test_num)
            results["graph_size"].append(n)
            results["theta_FF"].append(theta_FF)
            results["theta_PR"].append(theta_PR)
            results["theta_MIN"].append(theta_MIN if theta_MIN is not None else 0)

    return results


# Plot runtime results by graph size
def plot_results_by_graph_size(results, n_values):
 
    # Initialize lists to store average execution times
    avg_theta_FF = []
    avg_theta_PR = []
    avg_theta_MIN = []

    for n in n_values:
        # Filter results for the current graph size
        indices = [i for i, size in enumerate(results["graph_size"]) if size == n]
        theta_FF = [results["theta_FF"][i] for i in indices]
        theta_PR = [results["theta_PR"][i] for i in indices]
        theta_MIN = [results["theta_MIN"][i] for i in indices]

        # Compute average execution times
        avg_theta_FF.append(sum(theta_FF) / len(theta_FF))
        avg_theta_PR.append(sum(theta_PR) / len(theta_PR))
        avg_theta_MIN.append(sum(theta_MIN) / len(theta_MIN))

    # Plot average execution times
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, avg_theta_FF, label="Ford-Fulkerson", color="blue", marker="o")
    plt.plot(n_values, avg_theta_PR, label="Push-Relabel", color="red", marker="o")
    plt.plot(n_values, avg_theta_MIN, label="Min-Cost Flow", color="green", marker="o")

    # Add labels, title, and legend
    plt.xlabel("Graph Size (n)")
    plt.ylabel("Average Execution Time (s)")
    plt.title("Average Execution Time by Graph Size")
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()


if __name__ == "__main__":
    n_values = [10, 20, 40, 100, 1000]
    results = analyze_complexity()
    plot_results_by_graph_size(results, n_values)
