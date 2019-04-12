Tutorial
=============
OrthoEvolution has been built with Python 3.5 (and up) as a multi-faceted package and pipeline
framework for comparative genetics in order to infer orthologous genes.

Currently, this python package is comprised of 5 major modules:

1. [Cookies Module](#using-the-cookies-module) - Project structure creation using cookiecutter.
2. [Manager Module](#using-the-manager-module) - Configuration management as well project deployment.
3. [Orthologs Module](#using-the-orthologs-module) - Tools for comparative genetics analysis including alignment analysis and phylogenetics.
4. [Pipeline Module](#using-the-pipeline-module) - Various preconfigured pipelines to be used in orthology inference.
5. [Tools Module](#using-the-tools-module) - Utilities that aid in ftp downloading, server communication, and reusable everyday functions

When used together, these 4 modules offer a cohesive environment for easily creating,
managing, and deploying a bioinformatics pipeline for orthologous genes/species.  In the future
these tools will also be accessible from the command line and from a web application.

READMEs are provided in each module's directory, but we've compiled a mini tutorial here
that can inform users on how to use these modules.


## Using the Cookies module

### Overview
The Cookies module acts as a repository for custom [cookiecutter](https://github.com/audreyr/cookiecutter) templates.

Each "CookBook" allows us to quickly create and deploy different projects with various directory structures.  They are meant to help organize projects
and data in a standardized way.  This module is used almost extensively by the Manager module.

In the context of the Manager module the CookBook class is used to deploy an entire repository geared towards developing a web-page using Flask and R-Shiny.
Cookies can also be used to create standalone projects that don't require an entire repository.


* Templates used when creating a full repository:
  * _Cookies/new_repository_
  * _Cookies/new_user_
  * _Cookies/new_project_
  * _Cookies/new_research_
  * _Cookies/new_database_ (for NCBI, proprietary, etc. databases)
  * _Cookies/new_app_ (for [R-Shiny](https://github.com/grabear/awesome-rshiny) applications)
  * _Cookies/new_website_ (for [Flask](http://flask.pocoo.org/) applications)

* Template for standalone projects
  * _Cookies/new_basic_project_

### Examples

```python
from OrthoEvol.Cookies import Oven
from pathlib import Path
import os

# Create the names used.
home = os.getcwd()
repo = "Development"
user = "RAG"
project = "Ortholog"
research = "GPCR"
research_type = "Comparative Genetics"
# Create the paths used
repo_path = Path(home) / Path(repo)
user_path = repo_path / Path('users')
project_path = user_path / Path(user) / Path('projects')
research_path = project_path / Path(project)

# Initialize the Oven object to create a full repository
Full_Kitchen = Oven(repo=repo, user=user, project=project, basic_project=False, output_dir=home)
# Create the new project
Full_Kitchen.bake_the_repo()
Full_Kitchen.bake_the_user(cookie_jar=user_path)
Full_Kitchen.bake_the_project(cookie_jar=project_path)
Full_Kitchen.bake_the_research(research=research, research_type=research_type, cookie_jar=research_path)

# Initialize the Oven object to setup a basic project
Basic_Kitchen = Oven(project=project, basic_project=True, output_dir=home)
# Create the new project
Basic_Kitchen.bake_the_project()
```

## Using the Manager module

### Overview
The Manager module uses the CookBook class in order to deploy a bioinformatics repository
with an organized directory structure based on specific users and the projects that they create.
Pipeline customization and configuration will also be possible through YAML files.

### Future Direction
First, a database_management class for dealing with the various databases (NCBI, BioSQL, etc.) will be developed.
Then the Management class will become responsible for functioning alongside Flask in order to create a web interface.
The web interface will give each user access to the Tools and Orthologs modules as well as data generated by the pipeline functionality.

### Examples
```python
# Manager classes can be used explicitly, or...
from OrthoEvol.Manager.management import Management
from OrthoEvol.Manager.management import RepoManagement
from OrthoEvol.Manager.management import UserManagement
from OrthoEvol.Manager.management import WebsiteManagement
from OrthoEvol.Manager.management import ProjectManagement

# ...they can be use implicitly through the main pipeline class.
from OrthoEvol.Manager.data_management import DataMana
```

#### Explicit Usage
```python
from OrthoEvol.Manager.management import ProjectManagement
# Use the flags to create a new repository/user/project/research directory system
pm = ProjectManagement(repo="repository1", user='user1', project='project1', research='research1',
    research_type='comparative_genetics', new_repo=True, new_user=True, new_project=True, new_research=True)
# Access the path variables
print(pm.research_path)
print(pm.research)
print(pm.Pantry.research_cookie)
```
#### Implicit Usage
```python
from OrthoEvol.Manager.data_management import DataMana
# Use a prebuilt configuration file in Manager/config/
# *start* a *new* project automatically
# This builds everything and then starts the pipeline
import os
pipeline = DataMana(pipeline='Ortho_CDS_1', project_path=os.getcwd(), start=True, new=True)
```
## Using the Orthologs Module

### Overview
The Orthologs module is the central data processing unit of our package.  Any published data will be generated using these submodules.

The sub modules are used for BLASTing NCBI's refseq database to discover orthologous genes,
parsing and analyzing BLASTn data, generating GenBank files for the orthologs, generating sequence data
for the orthologs, aligning the orthologous sequences for each gene, generating phylogenetic trees for each gene,
and doing phylogenetic analysis for each gene.

### Examples
```python
from OrthoEvol.Manager.management import ProjectManagement
from OrthoEvol.Orthologs.Blast.blastn_comparative_genetics import OrthoBlastN
from OrthoEvol.Orthologs.GenBank.genbank import GenBank
from OrthoEvol.Orthologs.Align.msa import MultipleSequenceAlignment as MSA

# In a real situation a dictionary configuration from YAML files will be used
# However a dictionary can be manually set up by the user within the script
# See the config files in Manager/config or use data_management.py as an example
management_cfg = mlast_cfg = genbank_cfg = alignment_cfg = {}

# Initialize the Project Manager
proj_mana = ProjectManagement(**management_cfg)

# Initialize the BLAST tool
# Compose this class with the Project Manager
myblast = OrthoBlastN(proj_mana=proj_mana, **management_cfg, **blast_cfg)
myblast.blast_config(myblast.blast_human, 'Homo_sapiens', auto_start=True)

# Initialize the GenBank parser
# Compose this class with the BLAST tool
# Implicitly uses the Project Manager as well
genbank = GenBank(blast=blast, **management_cfg, **genbank_cfg)
# Use the Blast tool data to get the desired GenBank files
genbank.blast2_gbk_files(myblast.org_list, myblast.gene_dict)

# Initialize the Aligner
# Compose this class with the GenBank parser
# Implicitly uses the Project Manager and the BLAST tool as well
al = MSA(genbank=genbank, **management_cfg, **alignment_cfg)
al.align(alignment_config['kwargs'])  # Underdeveloped

```
## Using the Pipeline module
The pipeline module integrates the python package [luigi](#) with our package to
create a pipeline that is accessible via the command-line and can be utilized
with a qsub/pbs job scheduling system.

### Examples

## Using the Tools module
The tools module is a grouping of utilities used by our package.  While they
could have be stored in each modules util.py file, they were used and developed
on a global scale, and hence required their own module.


### Overview
Some of the tools/classes in the tools module are:

- `NcbiFTPClient` - provides functions to easily download ncbi databases/files and update them.
- `LogIt` - A wrapper around logzero for easy logging to the screen or a file.
- `Multiprocess` - A simple and effective class that allows the input of a function
to map to a user's list in order to take advantage of parallel computing.
- `SGEJob` - A class to aid in submission of a job via `qsub` on a cluster.
- `Qstat` - A class that parses the output of `qstat` to return job information.
It also waits on job completion.
- `Slackify` -
- `MyGene` -

Can I integrate these tools with each other and with orther modules including my own?
**YES!** We'll provide some examples below!

### Examples

```python
# Import a tools module
from OrthoEvol.Tools import Slackify

# Slack takes a config file thats already set up
slack = Slackify(slackconfig='path/to/slackconfig.cfg')

# Message a channel and link to a user.

message_to_channel = 'Hey, <@username>. This is an update for the current script.'
slack.send_msg(channel='channelname', message=message_to_channel)
```
For more information, view the [slackify readme](https://github.com/OrthoEvolution/OrthoEvol-Scripts/tree/master/OrthoEvolution/Tools/slackify/README.md).