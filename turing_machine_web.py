from flask import Flask, request, jsonify
from turing_machine import TuringMachine, Transition

app = Flask(__name__)

# Simple binary increment machine transitions
TRANSITIONS = {
    ('s0', '0'): Transition('s0', '0', 'R'),
    ('s0', '1'): Transition('s0', '1', 'R'),
    ('s0', ' '): Transition('s1', ' ', 'L'),
    ('s1', '1'): Transition('s1', '0', 'L'),
    ('s1', '0'): Transition('halt', '1', 'N'),
    ('s1', ' '): Transition('halt', '1', 'N'),
}

@app.route("/")
def index():
    return (
        "<p>Turing Machine Web Interface</p>"
        "<p>Use /run?tape=1011 to increment a binary number.</p>"
    )

@app.route("/run")
def run_machine():
    tape = request.args.get("tape", "")
    machine = TuringMachine(TRANSITIONS, 's0')
    machine.load_tape(tape)
    result = machine.run()
    return jsonify({"input": tape, "output": result})


if __name__ == "__main__":
    app.run()
