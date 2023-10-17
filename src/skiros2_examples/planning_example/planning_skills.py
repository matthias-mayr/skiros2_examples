from skiros2_skill.core.skill import SkillDescription, SkillBase, ParamOptions, SerialStar
from skiros2_common.core.params import ParamTypes
from skiros2_common.core.world_element import Element

#################################################################################
# Description
#################################################################################

class Locate(SkillDescription):
    def createDescription(self):
        #=======Params=========
        self.addParam("Container", Element("skiros:Location"), ParamTypes.Required)
        self.addParam("Object", Element("skiros:Product"), ParamTypes.Optional)
        self.addParam("Camera", Element("skiros:DepthCamera"), ParamTypes.Required, [ParamOptions.Lock])
        #=======PreConditions=========
        self.addPreCondition(self.getRelationCond("RobotAt", "skiros:at", "Robot", "Container", True))
        self.addPreCondition(self.getAbstractRelationCond("ContainerForObject", "skiros:partReference", "Container", "Object", True))
        #=======PostConditions=========
        self.addPostCondition(self.getRelationCond("InContainer", "skiros:contain", "Container", "Object", True))
        self.addPostCondition(self.getHasPropCond("HasPosition", "skiros:Position", "Object", True))


class Drive(SkillDescription):
    def createDescription(self):
        # =======Params=========
        self.addParam("Robot", Element("cora:Robot"), ParamTypes.Required)
        self.addParam("TargetLocation", Element("skiros:Location"), ParamTypes.Required)
        self.addParam("Velocity", 0.5, ParamTypes.Optional)
        self.addParam("StartLocation", Element("skiros:Location"), ParamTypes.Inferred)
        # =======PreConditions=========
        self.addPreCondition(self.getRelationCond("RobotAt", "skiros:at", "Robot", "StartLocation", True))
        # =======PostConditions=========
        self.addPostCondition(self.getRelationCond("NoRobotAt", "skiros:at", "Robot", "StartLocation", False))
        self.addPostCondition(self.getRelationCond("RobotAt", "skiros:at", "Robot", "TargetLocation", True))


class Pick(SkillDescription):
    def createDescription(self):
        #=======Params=========
        self.addParam("Container", Element("skiros:Location"), ParamTypes.Inferred)
        self.addParam("Object", Element("skiros:Product"), ParamTypes.Required)
        self.addParam("Arm", Element("rparts:ArmDevice"), ParamTypes.Required)
        self.addParam("Gripper", Element("rparts:GripperEffector"), ParamTypes.Inferred)
        #=======PreConditions=========
        self.addPreCondition(self.getPropCond("EmptyHanded", "skiros:ContainerState", "Gripper", "=", "Empty", True))
        self.addPreCondition(self.getRelationCond("ObjectInContainer", "skiros:contain", "Container", "Object", True))
        #=======HoldConditions=========
        self.addHoldCondition(self.getRelationCond("RobotAtLocation", "skiros:at", "Robot", "Container", True))
        #=======PostConditions=========
        self.addPostCondition(self.getPropCond("EmptyHanded", "skiros:ContainerState", "Gripper", "=", "Empty", False))
        self.addPostCondition(self.getRelationCond("Holding", "skiros:contain", "Gripper", "Object", True))

class Place(SkillDescription):
    def createDescription(self):
        #=======Params=========
        self.addParam("PlacingLocation", Element("skiros:Location"), ParamTypes.Required)
        self.addParam("Arm", Element("rparts:ArmDevice"), ParamTypes.Required)
        self.addParam("Gripper", Element("rparts:GripperEffector"), ParamTypes.Inferred)
        self.addParam("Object", Element("skiros:Product"), ParamTypes.Inferred)
        #=======PreConditions=========
        self.addPreCondition(self.getRelationCond("Holding", "skiros:contain", "Gripper", "Object", True))
        #=======HoldConditions=========
        self.addHoldCondition(self.getRelationCond("RobotAtLocation", "skiros:at", "Robot", "PlacingLocation", True))
        #=======PostConditions=========
        self.addPostCondition(self.getPropCond("EmptyHanded", "skiros:ContainerState", "Gripper", "=", "Empty", True))
        self.addPostCondition(self.getRelationCond("NotHolding", "skiros:contain", "Gripper", "Object", False))
        self.addPostCondition(self.getRelationCond("InPlace", "skiros:contain", "PlacingLocation", "Object", True))

#################################################################################
# Implementation
#################################################################################


class locate_fake(SkillBase):
    def createDescription(self):
        self.setDescription(Locate(), self.__class__.__name__)

    def expand(self, skill):
        skill(
            self.skill("Wait", "wait", specify={"Duration": 1.0}),
        )


class drive_fake(SkillBase):
    def createDescription(self):
        self.setDescription(Drive(), self.__class__.__name__)

    def expand(self, skill):
        skill.setProcessor(SerialStar())
        skill(
            self.skill("Wait", "wait", specify={"Duration": 1.0}),
            self.skill("WmSetRelation", "wm_set_relation", remap={'Src': "Robot", 'Dst': "StartLocation", },
                       specify={'Relation': 'skiros:at', 'RelationState': False}),
            self.skill("WmSetRelation", "wm_set_relation", remap={'Src': "Robot", 'Dst': "TargetLocation"},
                       specify={'Relation': 'skiros:at', 'RelationState': True})
        )


class drive_platform(SkillBase):
    def createDescription(self):
        self.setDescription(Drive(), self.__class__.__name__)

    def expand(self, skill):
        skill.setProcessor(SerialStar())
        skill(
            self.skill("MovePlatform", "", specify={"Velocity": self.params["Velocity"].values}),
            self.skill("WmSetRelation", "wm_set_relation", remap={'Src': "Robot", 'Dst': "StartLocation", },
                       specify={'Relation': 'skiros:at', 'RelationState': False}),
            self.skill("WmSetRelation", "wm_set_relation", remap={'Src': "Robot", 'Dst': "TargetLocation"},
                       specify={'Relation': 'skiros:at', 'RelationState': True})
        )


class drive_platform(SkillBase):
    def createDescription(self):
        self.setDescription(Drive(), self.__class__.__name__)

    def expand(self, skill):
        skill.setProcessor(SerialStar())
        skill(
            self.skill(SelectorStar())(
                self.skill("MovePlatformDirect", "", specify={"Velocity": self.params["Velocity"].values}),
                self.skill("MovePlatformPlanning", "", specify={"Velocity": self.params["Velocity"].values}),
            ),
            self.skill("WmSetRelation", "wm_set_relation", remap={'Src': "Robot", 'Dst': "StartLocation", },
                       specify={'Relation': 'skiros:at', 'RelationState': False}),
            self.skill("WmSetRelation", "wm_set_relation", remap={'Src': "Robot", 'Dst': "TargetLocation"},
                       specify={'Relation': 'skiros:at', 'RelationState': True})
        )


class drive_platform(SkillBase):
    def createDescription(self):
        self.setDescription(Drive(), self.__class__.__name__)

    def expand(self, skill):
        skill.setProcessor(SerialStar())
        skill(
            self.skill(SelectorStar())(
                self.skill("MovePlatformDirect", "", specify={"Velocity": self.params["Velocity"].values}),
                self.skill("MovePlatformPlanning", "", specify={"Velocity": self.params["Velocity"].values}),
            ),
            self.skill("VerifyPlatformArrival", ""),
            self.skill("WmSetRelation", "wm_set_relation", remap={'Src': "Robot", 'Dst': "StartLocation", },
                       specify={'Relation': 'skiros:at', 'RelationState': False}),
            self.skill("WmSetRelation", "wm_set_relation", remap={'Src': "Robot", 'Dst': "TargetLocation"},
                       specify={'Relation': 'skiros:at', 'RelationState': True})
        )


class pick_fake(SkillBase):
    def createDescription(self):
        self.setDescription(Pick(), self.__class__.__name__)

    def expand(self, skill):
        skill(
            self.skill("Wait", "wait", specify={"Duration": 1.0}),
            self.skill("WmMoveObject", "wm_move_object",
                remap={"StartLocation": "Container", "TargetLocation": "Gripper"}),
        )

class place_fake(SkillBase):
    def createDescription(self):
        self.setDescription(Place(), self.__class__.__name__)

    def expand(self, skill):
        skill(
            self.skill("Wait", "wait", specify={"Duration": 1.0}),
            self.skill("WmMoveObject", "wm_move_object",
                remap={"StartLocation": "Gripper", "TargetLocation": "PlacingLocation"}),
        )


