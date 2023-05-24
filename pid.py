import json
import mist
import sens
import time

class PIDController:
    def __init__(self, Kp, Ki, Kd, setpoint):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.time = time.time()
        self.last_time = self.time - 60.0
        self.error = 0
        self.last_error = 0
        self.integral = 0
        self._load()

    def update(self, feedback):
        self.time = time.time()
        dt = self.time - self.last_time
        self.error = self.setpoint - feedback
        self.integral += self.error * dt
        derivative = (self.error - self.last_error) / dt if dt > 0 else 0
        output = self.Kp * self.error + self.Ki * self.integral + self.Kd * derivative
        self.last_error = self.error
        self.last_time = self.time
        self._dump()
        self.debug(self.error, self.integral, derivative, output)
        return output

    def debug(self, error, integral, derivative, output):
        fp = open('debug.json', 'w')
        data = {'error': error, 'integral': integral, 'derivative': derivative, 'output': output}
        json.dump(data, fp)
        fp.close()

    def _dump(self):
        fp = open('pid.json', 'w')
        data = {'time': self.time, 'error': self.error, 'integral': self.integral}
        json.dump(data, fp)
        fp.close()

    def _load(self):
        try:
            fp = open('pid.json')
            data = json.load(fp)
            self.last_time = data['time']
            self.last_error = data['error']
            self.integral = data['integral']
            fp.close()
            if (time.time() - self.last_time) > 300:
                raise Exception('stale cache file')
        except Exception as e:
            self.last_time = time.time() - 60.0
            self.last_error = 0
            self.integral = 0
            print("Exception: {}".format(e))

if __name__ == "__main__":
    # Initialize the PID controller
    pid = PIDController(Kp=1.0, Ki=0.005, Kd=0.0, setpoint=85.0)

    # Set up the process
    process_value = 0.0
    t = 0.0
    dt = 60

    # Control the process using the PID controller
    for i in range(100):
        data = sens.query()
        process_value = data.humidity

        # Update the PID controller with the current feedback and time step
        control_value = pid.update(feedback=process_value)

        # Print the results
        print(f"Time: {t:.1f}, Setpoint: {pid.setpoint:.1f}, Feedback: {process_value:.1f}, Control: {control_value:.1f}")

        if control_value > (dt - 1.0):
            control_value = dt - 1.0
        elif control_value < 0.1:
            control_value = 0.0

        # Apply the control value to the process and get the new feedback
        if control_value > 0.1:
            mist.pulse(control_value)

        time.sleep(dt - control_value)

        # Increment the time
        t += dt
