from skiros2_skill.core.skill import SkillDescription
from skiros2_common.core.primitive import PrimitiveBase


class MyPrimitive(SkillDescription):
    def createDescription(self):
        self.addParam("Boolean", False, ParamTypes.Required)


class my_primitive(PrimitiveBase):
    def createDescription(self):
        """Set the primitive type"""
        self.setDescription(MyPrimitive())

    def onInit(self):
        """Called once when loading the primitive. If return False, the primitive is not loaded"""
        return True

    def onPreempt(self):
        """ Called when skill is requested to stop. """
        pass

    def onStart(self):
        """Called just before 1st execute"""
        return True

    def onEnd(self):
        """Called just after last execute"""
        pass

    def execute(self):
        """ Main execution function """
        return self.success("Done")