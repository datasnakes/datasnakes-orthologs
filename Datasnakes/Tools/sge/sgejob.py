import contextlib
from subprocess import run, CalledProcessError, PIPE
import os

from Datasnakes.Tools.sge import basejobids, writecodefile, import_temp
from Datasnakes.Tools.sgeconfig import __DEFAULT__, __CUSTOM__


class BaseJob(object):
    """Create a class for simple jobs."""
    def __init__(self):
        self.defaultjob = __DEFAULT__
        self.customjob = __CUSTOM__

    def _cleanup(base):
        """Clean up job scripts."""
        os.remove(base + '.pbs')
        os.remove(base + '.py')


class SGEJob(BaseJob):
    """Create multiple jobs & scripts for each job to run."""
    def __init__(self, jobname):
        self.baseid, self.base = self._configure(jobname)

    def _configure(self, jobname):
        """Configure job attributes or set it up."""
        baseid, base = basejobids(jobname)
        return baseid, base

    def submit(self, code, default=True):
        """Creates and submit a qsub job. Also uses python code."""
        # TIP If python is in your environment as only 'python' update that.
        # TODO-SDH add a default parameter or custom parameter
        # If default, a python file will be created from code that is used.
        if self.default == default:
            writecodefile(filename=self.base, code=code, language='python')

            # Create the pbs script from the template or dict
            pbstemp = import_temp('temp.pbs')

            attributes = __DEFAULT__

            with open(self.base + '.pbs', 'w') as pbsfile:
                pbsfile.write(pbstemp.substitute(attributes))
                pbsfile.close()
        else:
            raise NotImplementedError('Custom qsub jobs are forbidden.')
            # TODO Improve custom job creation
        #            pbstemp = self.import_temp('temp.pbs')
        #            with open(base + '.pbs', 'w') as pbsfile:
        #                pbsfile.write(pbstemp.substitute(self.pbs_dict))
        #                pbsfile.close()

        with contextlib.suppress(CalledProcessError):
            cmd = ['qsub ' + self.base + '.pbs']  # this is the command
            # Shell MUST be True
            cmd_status = run(cmd, stdout=PIPE, stderr=PIPE, shell=True)

            if cmd_status.returncode == 0:  # Command was successful.
                print('Job submitted.\n')
                # TODO add a check to for job errors or check for error file.

            else:  # Unsuccessful. Stdout will be '1'
                print("PBS job not submitted.")
#                _cleanup(base=base)
