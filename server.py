from flask import Flask , render_template, request, jsonify
from main import School, Graph, run_evolution

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('new_indexx.html')

@app.route('/oblicz-vrp', methods=['POST'])
def oblicz_vrp():
    dane = request.get_json()
    print("Otrzymano dane:", dane)
    params = dane['parametry']
    szkoly_z_js = dane['szkoly']

    nodes = []

    depot = School(id=0,x=300,y=30,profit=0,service_time=0,time_window_start=0,time_window_end=1000)
    nodes.append(depot)

    for s in szkoly_z_js:
        
        nowa_szkola = School(
            id=int(s['id']),
            x=float(s['x']),
            y=float(s['y']),
            profit=float(s['profit']),
            service_time=float(s['service_time']),
            time_window_start=float(s['time_window_start']),
            time_window_end=float(s['time_window_end']),
            visit_cost=0.0
        )
        nodes.append(nowa_szkola)

    graph = Graph(nodes, depot_id=0)

    wynik = run_evolution(
        graph,
        pop_size=int(params['pop_size']),
        generations=int(params['generations']),
        mutation_mode=params['mutation_mode'],
        mut_rates=params['mut_rates'],
        cross_mode=params['cross_mode']
    )
    return jsonify(wynik)


if __name__ == "__main__":
    app.run(debug=True)

