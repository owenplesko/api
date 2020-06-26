from django.test import TestCase, Client
from carbon_calculator.models import CalcUser, Event, Station, Action, Group, Question
from carbon_calculator.views import importcsv
from database.models import Vendor
from django.utils import timezone #For keeping track of when the consistency was last checked
import jsons
import OpenSSL
from carbon_calculator.solar import EvalSolarPV
import pprint

OUTPUTS_FILE   = "carbon_calculator/tests/expected_outputs.txt"
INPUTS_FILE    = "carbon_calculator/tests/Inputs.txt"
NEW_ACTION     = "New action"
REMOVED_ACTION = "Removed action"
VALUE_DIFF     = "Value difference"

# Create your tests here.
class CarbonCalculatorTest(TestCase):
    @classmethod
    def setUpClass(self):
        self.client = Client()
        self.differences = []
        self.got_outputs = True


        self.input_data = self.read_inputs(os.environ(TEST_INPUTS))
        self.output_data = []

    @classmethod
    def tearDownClass(self):
        print("tearDownClass")
        #populate_inputs_file()

        write_outputs(os.environ(TEST_OUTPUTS))

    def test_info_actions(self):
        # test routes function
        # test there are actions
        # test that one action has the average_points
    def get_consistency_files(self):
        """Return content needed for the consistency test"""
        got_inputs  = True
        got_outputs = True
        try:
            f = open(INPUTS_FILE, 'r')
            inputs = [eval(i.strip()) for i in f.readlines()]
            f.close()
        except FileNotFoundError:
            print("Could not find inputs file, aborting consistency check")
            got_inputs = False
            inputs = {}
        try:
            f = open(OUTPUTS_FILE, 'r')
            raw_prev_outputs = f.read() #No code to ensure this isn't empty yet
            prev_outputs = eval(raw_prev_outputs)
            f.close()
        except FileNotFoundError:
            f = open(OUTPUTS_FILE, "w")
            f.close()
            got_outputs = False
            prev_outputs = {}
        return got_inputs, got_outputs, inputs, prev_outputs

    def eval_all_actions(self, inputs):
        """Run the estimate method of all the actions of the Carbon Calculator."""
        output_data = {"Timestamp" : timezone.now().isoformat(" ")} #Time of last test
        for aip in inputs: #aip = action inputs pair
            try:
                output_data.update(
                    {aip["Action"] : jsons.loads( #Response of estimate in dict form
                        self.client.post(
                            "/cc/estimate/{}".format(aip['Action']), aip["inputs"]
                                ).content)}) #Throwing errors, need a better inputs file
            except Exception as e: #Some may throw errors w/o inputs
                pass #Don't clutter the screen
        return output_data

    def compare(self, new, old):
        """
        Compare the old set of results with the new set.

        Populate a list of differences (tuples) according to the following rules:
        For a new action (action found in new results aggregate but not old)
        ("New action", ACTION_NAME)
        For a removed action (action found in old results aggregate but not new)
        ("Removed action", ACTION_NAME)
        For a differing value between the two aggregates
        ("Value difference", NEW_VALUE, OLD_VALUE)
        """
        #print(new, old)
        differences = []
        new_actions = [i for i in new.keys()]
        old_actions = [i for i in old.keys()]
        print(new_actions, old_actions)
        shared_actions = [] #Actions that are in both lists, and can be compared
        for action in new_actions:
            if action is not "Timestamp":
                if action in old_actions:
                        shared_actions.append(action)
                        print("Shared action:", action)
                else:
                    differences.append((NEW_ACTION, action))
                    print("Not shared action:", action)
                    print(differences)
        for action in old_actions:
            if not action in new_actions and action is not "Timestamp":
                differences.append((REMOVED_ACTION, action))
                print(differences)
        print("Shared actions:", shared_actions)
        for action in shared_actions:
            for result_aspect in new[action].keys(): #status, points, cost, etc
                if not new[action][result_aspect] == old[action][result_aspect]:
                    differences.append((
                        VALUE_DIFF,
                        result_aspect,
                        new[action][result_aspect],
                        old[action][result_aspect]))
        print("Differences in compare:", differences)
        return differences

    def dump_outputs(self, outputs):
        """Dump the outputs of all the CC method calls into the OUTPUTS_FILE"""
        f = open(OUTPUTS_FILE, "w")
        f.write(str(outputs))
        f.close()

    #def test_solarPVNoArgs(self):
    #    response = self.client.post('/cc/getInputs/install_solarPV', {})
    #    data = jsons.loads(response.content)
    #    #outputInputs(data)
    def pretty_print_diffs(self, diffs, oldtime, newtime):
        print("\nDifferences: " + str(diffs)) #Not pretty yet

    #def test_solarPVGreat(self):
    #    response = self.client.post('/cc/getInputs/install_solarPV',
    #        {
    #        'solar_potential': 'Great'
    #        }
    #    )
    #    data = jsons.loads(response.content)
    def test_consistency(self):
        """
        Test if the results of all estimation calls match those of the last run.

        Get the inputs to each method from the INPUTS_FILE, as well as the
        previous outputs from the OUTPUTS_FILE. Call all methods of the carbon
        calculator with the inputs retrieved earlier, and compare the results
        with the results of the last run. Finally, pretty print the differences
        between this test run and the last one. Don't return anything.
        """
        #Check for required files
        got_inputs, self.got_outputs, inputs, prev_outputs = self.get_consistency_files()
        if not got_inputs:
            return
        #Run evals for all values
        outputs = self.eval_all_actions(inputs)
        #Compare
        if self.got_outputs:
            self.differences = self.compare(outputs, prev_outputs)
        print("Differences in test_consistency: ", self.differences)
        self.dump_outputs(pprint.pformat(outputs))
        self.pretty_print_diffs(
            self.differences,
            prev_outputs["Timestamp"],
            outputs["Timestamp"])
def outputLine(data, filename, new=False):
    tag = "a"
    if new:
        tag = "w"

    f = open(filename, tag)
    f.write(str(data) + "\n")
    f.close()

def read_inputs(filename):
    data = []
    return data

def write_outputs(filename):
    outputLine(data,filename,True)
    pass


def get_all_action_names():
    client   = Client()
    response = client.get("/cc/info/actions")
    data     = jsons.loads(response.content)["actions"]
    return [i["name"] for i in data]

def populate_inputs_file():
    client      = Client()
    response    = client.get("/cc/info/actions")
    data        = jsons.loads(response.content)["actions"]
    names       = [i["name"] for i in data]

    filename_all = "carbon_calculator/tests/" + "allPossibleInputs.txt"
    outputInputs("# All Possible Calculator Inputs", filename_all, True)
    filename_def = "carbon_calculator/tests/" + "defaultInputs.txt"
    outputInputs("# Default Calculator Inputs", filename_def, True)
    np = 0    
    for name in names:
        # get info on the action to find allowed parameter values
        print("URL: /cc/info/action/{}".format(name))
        response = client.get("/cc/info/action/{}".format(name))
        data = response.json() #jsons.loads(response.content, {})
        actionName = data["action"]["name"]

        questions = data["action"]["questionInfo"]
        qTot = []
        qInd = []
        for question in questions:
            qType = question["questionType"]
            qInd.append(0)
            if qType == "Choice":
                qTot.append(len(question["responses"]))
            else:
             if qType == "Number":
                qTot.append(1)
             else:
                qTot.append(0)

        nq = len(questions)
        qr = range(nq)
        done = False
        ni = 0
        while not done:
            actionPars = {"Action": actionName}
            q = 0
            for q in qr:
                question = questions[q]
                if qTot[q] > 1:
                    actionPars[question["name"]] = question["responses"][qInd[q]]["text"]
                else:
                    if qTot[q] == 1:
                        actionPars[question["name"]] = 0

            outputInputs(actionPars, filename_all)
            np += 1
            ni += 1

            # update the response indices, increment one by one to get each combination
            for q in qr:
                if qTot[q]>0:
                    qInd[q] += 1
                    if qInd[q] == qTot[q]:
                        qInd[q] = 0
                    else:
                        break
                if q == nq-1:
                    done = True

        msg = "Action '%s', %d possible inputs" % (actionName, ni)
        print(msg)

        #generate the default values list
        try:
            outputInputs(
                jsons.loads(
                    client.post(
                        "/cc/getInputs/{}".format(name), {}
                        ).content
                    ),
                    filename_def
                )
        except:
            pass

    msg = "Number possible calculator inputs with all choices = %d" % np
    print(msg)
