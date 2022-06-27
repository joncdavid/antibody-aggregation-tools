#!/usr/bin/env python3

import sys

from experiment_parameters import ExperimentParameters
from experiment_declaration import ExperimentDeclaration
from genf_generic import GenFileGeneric


class GenFileExperimentNameDotXml(GenFileGeneric):
    def __init__(self, exp_params ):
        super().__init__( exp_params )

    def _write_header(self, fout, template_file):
        experimentName = self.p.experimentName
        totalNumMolecules = self._get_totalNumMolecules()
        pos_dof_val = 3 * totalNumMolecules
        dofs_val = 2 * pos_dof_val

        s1 = "__TMPL_EXP_NAME__"
        s2 = "__TMPL_POS_DOF__"
        s3 = "__TMPL_DOFS__"

        fin = open(template_file, "r")
        for line in fin:
            line = line.replace( s1, experimentName )
            line = line.replace( s2, str(pos_dof_val) )
            line = line.replace( s3, str(dofs_val) )
            fout.write( line )
        fin.close()


    def _write_body(self, f):
        minXZ = self.p.minXZ
        maxXZ = self.p.maxXZ
        minY = -50
        maxY = 200
        totalNumMolecules = self._get_totalNumMolecules()
        for index in range(0,3*totalNumMolecules):
            (r,label) = _get_label( index )
            if (r == 1):
                minVal = minY
                maxVal = maxY
            elif (r == 0) or (r == 2):
                minVal = minXZ
                maxVal = maxXZ
            else:
                raise Exception("[ERROR], should not reach this section.")
            f.write( "<parameter id=\"{}\" Label=\"{}\" type=\"translational\" min=\"{}\" max=\"{}\" />\n".format(index, label, minVal, maxVal) )


    def _write_footer(self, fout, template_file):
        seed = self.p.seed
        timesteps = self.p.maxTimesteps
        s1 = "__TMPL_SEED__"
        s2 = "__TMPL__TIMESTEPS__"
        fin = open(template_file, "r")
        for line in fin:
            line = line.replace( s1, str(seed) )
            line = line.replace( s2, str(timesteps) )
            fout.write( line )
        fin.close()
        
        return

    def write_file(self, fname, template_header, template_footer):
        f = open(fname, "w")

        self._write_header(f, template_header)
        self._write_body(f)
        self._write_footer(f, template_footer)
        
        f.close()

## end of class

def _get_label(index):
    r_dict = { 0:"x", 1:"y", 2:"z" }
    moleculeTypeID = index // 3
    r = index % 3
    component = r_dict[r]
    label = "{}{}".format(component, moleculeTypeID)
    return (r,label)
    

if __name__ == "__main__":
    fname = sys.argv[1]
    ftemplate_header = sys.argv[2]
    ftemplate_footer = sys.argv[3]
    
    d = ExperimentDeclaration()
    p = d.load_from_file(fname)

    genf = GenFileExperimentNameDotXml( p )
    genf.write_file("experimentName.xml", ftemplate_header, ftemplate_footer)
