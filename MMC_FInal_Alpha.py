
import collections
from json.decoder import JSONDecodeError
import re

from PIL import Image
from PIL.ImageQt import ImageQt

import os
import sys
import shutil

from pathlib import Path

import json
from PySide6 import QtGui
import hjson

from PySide6 import QtWidgets
from PySide6.QtCore import QPoint, QRect, QDir, QAbstractTableModel, QTime, QTimer
from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QFileSystemModel, QDockWidget, QFocusFrame, QFrame, QLabel, QLayout, QLineEdit, QListWidget, QMainWindow, QMenu, QMenuBar, QPushButton, QStyle, QStyleOptionTitleBar, QTabWidget, QTreeView, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QCheckBox, QScrollArea, QHBoxLayout, QGridLayout, QComboBox, QTextEdit, QToolBar, QGraphicsTextItem, QGraphicsItem
from PySide6.QtGui import QPainter, QColor, QFont, QPixmap, QFontDatabase, QTextLine, QAction
from hjson.scanner import HjsonDecodeError



window_close = True

window = None
MaiL = None

WS = 0
TempMod = None

attachebleWidgets = []

_tempButtonContent = None

TempZipPath = ""
ContentObject = {"Mod": {}, "Path": None, "Type": ["", ""], "Text": ""}
RootMod = [{}, ""]
EditRoot = [0, ""]

StyleSheetList = ["QPushButton { font-family: fontello; font-size: 10 px; background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover {border-color: #ffd37f;} QFrame { font-family: fontello; font-size: 10 px; background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; }", 
				  "QPushButton { background-color:#00000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover { background-color:#00000000; border-style: solid; border-width: 3px; border-color: #ffd37f; color: #ffffff; }", 
				  "QPushButton { background-color:#000000; border-style: solid; border-width: 1px; border-color: #454545; color: #ffffff; } QPushButton:hover { background-color:#000000; border-style: solid; border-width: 1px; border-color: #ffd37f; color: #ffffff; } QPushButton:disabled { background-color:#000000; border-style: solid; border-width: 1px; border-color: #84f490; color: #ffffff; }"]


classType = {
	"mod": {"name": "Name", "displayName": "DisplayName", "description": "Description", "author": "Author", "version": "0.1", "minGameVersion": "105", "dependencies": [], "hidden": False},
	
	"UnlockableContent": {"name": "Name", "localizedName": "Local Name", "description": "Description", "fullIcon": None, "generateIcons": True, "hideDetails": False, "iconId": -1, "inlineDescription": True, "alwaysUnlocked": True},

	"Block": {"extend": "UnlockableContent", "hasItems": False, "hasLiquids": False, "hasPower": False, "outputsLiquid": False, "consumesPower": True, "outputsPower": False, "conductivePower": False, "outputsPayload": False, "acceptsPayload": False, "acceptsItems": False, "separateItemCapacity": False, "itemCapacity": 10, "liquidCapacity": 10.0, "liquidPressure": 1.0, "outputFacing": True, "noSideBlend": False, "displayFlow": True, "inEditor": True, "lastConfig": None, "saveConfig": False, "copyConfig": True, "clearOnDoubleTap": False, "update": False, "destructible": False, "unloadable": True, "isDuct": False, "allowResupply": False, "solid": False, "solidifes": False, "teamPassable": False, "underBullets": False, "rotate": False, "rotateDraw": True, "invertFlip": False, "variants": 0, "drawArrow": True, "drawTeamOverlay": True, "saveData": False, "breakable": False, "rebuildable": True, "privileged": False, "requiresWater": False, "placeableLiquid": False, "placeablePlayer": True, "placeableOn": True, "insulated": False, "squareSprite": True, "absorbLasers": False, "enableDrawStatus": True, "drawDisabled": True, "autoResetEnabled": True, "noUpdateDisabled": False, "updateInUnits": True, "alwaysUpdateInUnits": False, "useColor": True, "itemDrop": None, "playerUnmineable": False, "attributes": None, "scaledHealth": -1.0, "health": -1, "armor": 0.0, "baseExplosiveness": 0.0, "destroyBullet": None, "drawCracks": True, "createRubble": True, "floating": False, "size": 1, "offset": 0.0, "sizeOffset": 0, "clipSize": -1.0, "placeOverlapRange": 50.0, "crushDamageMultiplier": 1.0, "timers": 1, "cacheLayer": "normal", "fillsTile": True, "forceDark": False, "alwaysReplace": False, "replaceable": True, "group": None, "flags": "of()", "priority": 0.0, "unitCapModifier": 0, "configurable": False, "commandable": False, "allowConfigInventory": True, "logicConfigurable": False, "consumesTap": False, "drawLiquidLight": True, "envRequired": 0, "envEnabled": 1, "envDisabled": 0, "sync": False, "conveyorPlacement": False, "allowDiagonal": True, "swapDiagonalPlacement": False, "schematicPriority": 0, "mapColor": "000000ff", "hasColor": False, "targetable": True, "attacks": False, "suppressable": False, "canOverdrive": True, "outlineColor": "404049ff", "outlineIcon": False, "outlineRadius": 4, "outlinedIcon": -1, "hasShadow": True, "customShadow": False, "placePitchChange": True, "breakPitchChange": True, "placeSound": "place", "breakSound": "breaks", "destroySound": "boom", "albedo": 0.0, "lightColor": "ffffffff", "emitLight": False, "lightRadius": 60.0, "fogRadius": -1, "loopSound": None, "loopSoundVolume": 0.5, "ambientSound": None, "ambientSoundVolume": 0.05, "requirements": [], "category": "distribution", "buildCost": 20.0, "buildVisibility": "hidden", "buildCostMultiplier": 1.0, "deconstructThreshold": 0.0, "instantDeconstruct": False, "breakEffect": "breakBlock", "destroyEffect": "dynamicExplosion", "researchCostMultiplier": 1.0, "researchCostMultipliers": None, "researchCost": None, "instantTransfer": False, "quickRotate": True, "subclass": None, "highUnloadPriority": False, "selectScroll": 0.0, "buildType": None, "configurations": None, "itemFilter": [], "liquidFilter": [], "consumers": [], "optionalConsumers": [], "nonOptionalConsumers": [], "updateConsumers": [], "hasConsumers": False, "consPower": None, "regionRotated1": -1, "regionRotated2": -1, "region": None, "editorIcon": None, "customShadowRegion": None, "teamRegion": None, "teamRegions": None, "variantRegions": None, "variantShadowRegions": None},

		"Accelerator": {"extend": "Block", "arrowRegion": None, "launching": "coreNucleus", "capacities": []},
		"Floor": {"extend": "Block", "edge": "stone", "speedMultiplier": 1.0, "dragMultiplier": 1.0, "damageTaken": 0.0, "drownTime": 0.0, "walkEffect": None, "walkSound": None, "walkSoundVolume": 0.1, "walkSoundPitchMin": 0.8, "walkSoundPitchMax": 1.2, "drownUpdateEffect": "bubble", "status": None, "statusDuration": 60.0, "liquidDrop": None, "liquidMultiplier": 1.0, "isLiquid": False, "overlayAlpha": 0.65, "supportsOverlay": False, "shallow": False, "blendGroup": "this", "oreDefault": False, "oreScale": 24.0, "oreThreshold": 0.828, "wall": "air", "decoration": "air", "canShadow": True, "needsSurface": True, "allowCorePlacement": False, "wallOre": False, "blendId": -1},
			"AirBlock": {"extend": "Floor"},
			"EmptyFloor": {"extend": "Floor"},
			"ShallowLiquid": {"extend": "Floor", "liquidBase": None, "floorBase": None, "liquidOpacity": 0.35},
			"OverlayFloor": {"extend": "Floor"},
				"OreBlock": {"extend": "OverlayFloor"},
		"LiquidBlock": {"extend": "Block", "liquidRegion": None, "topRegion": None, "bottomRegion": None},
			"LiquidJunction": {"extend": "LiquidBlock"},
			"LiquidRouter": {"extend": "LiquidBlock", "liquidPadding": 0.0},

			"Pump": {"extend": "LiquidBlock", "pumpAmount": 0.2, "consumeTime": 300.0, "drawer": None},
				"SolidPump": {"extend": "Pump", "result": "water", "updateEffect": None, "updateEffectChance": 0.02, "rotateSpeed": 1.0, "baseEfficiency": 1.0, "attribute": None, "rotatorRegion": None},
					"Fracker": {"extend": "SolidPump", "itemUseTime": 100.0},
			"Conduit": {"extend": "LiquidBlock", "timerFlow": 1, "botColor": "565656ff", "topRegions": None, "botRegions": None, "capRegion": None, "rotateRegions": None, "leaks": True, "junctionReplacement": None, "bridgeReplacement": None, "rotBridgeReplacement": None},
				"ArmoredConduit": {"extend": "Conduit"},
		"Conveyor": {"extend": "Block", "regions": None, "speed": 0.0, "displayedSpeed": 0.0, "junctionReplacement": None, "bridgeReplacement": None},
			"ArmoredConveyor": {"extend": "Conveyor"},
		"GenericCrafter": {"extend": "Block", "outputItem": None, "outputItems": None, "outputLiquid": None, "outputLiquids": None, "liquidOutputDirections": [-1], "dumpExtraLiquid": True, "ignoreLiquidFullness": False, "craftTime": 80.0, "craftEffect": None, "updateEffect": None, "updateEffectChance": 0.04, "warmupSpeed": 0.019, "legacyReadWarmup": False, "drawer": None},
			"AttributeCrafter": {"extend": "GenericCrafter", "attribute": "heat", "baseEfficiency": 1.0, "boostScale": 1.0, "maxBoost": 1.0, "minEfficiency": -1.0, "displayEfficiencyScale": 1.0, "displayEfficiency": True},
			"HeatCrafter": {"extend": "GenericCrafter", "heatRequirement": 10.0, "overheatScale": 1.0, "maxEfficiency": 4.0},
			"HeatProducer": {"extend": "GenericCrafter", "heatOutput": 10.0, "warmupRate": 0.15},
		"Wall": {"extend": "Block", "lightningChance": -1.0, "lightningDamage": 20.0, "lightningLength": 17, "lightningColor": "f3e979ff", "lightningSound": "spark", "chanceDeflect": -1.0, "flashHit": False, "flashColor": "ffffffff", "deflectSound": None},
			"AutoDoor": {"extend": "Wall", "timerToggle": 1, "checkInterval": 20.0, "openfx": "dooropen", "closefx": "doorclose", "doorSound": "door", "openRegion": None, "triggerMargin": 12.0},
			"BaseShield": {"extend": "Wall", "radius": 200.0, "sides": 24},
			"Door": {"extend": "Wall", "timerToggle": 1, "openfx": "dooropen", "closefx": "doorclose", "doorSound": "door", "openRegion": None},
		"BaseTurret": {"extend": "Block", "range": 80.0, "placeOverlapMargin": 56.0, "rotateSpeed": 5.0, "coolEffect": "fuelburn", "coolantMultiplier": 5.0, "coolant": None},
			"BuildTurret": {"extend": "BaseTurret", "timerTarget": 1, "timerTarget2": 2, "targetInterval": 15, "baseRegion": None, "glowRegion": None, "buildSpeed": 1.0, "buildBeamOffset": 5.0, "unitType": None, "elevation": -1.0, "heatColor": "ffd37fe5"},
		"StorageBlock": {"extend": "Block", "coreMerge": True},
			"CoreBlock": {"extend": "StorageBlock", "thruster1": None, "thruster2": None, "thrusterLength": 3.5, "isFirstTier": False, "incinerateNonBuildable": False, "unitType": "alpha", "captureInvicibility": 900.0},
		"Drill": {"extend": "Block", "hardnessDrillMultiplier": 50.0, "tier": 0, "drillTime": 300.0, "liquidBoostIntensity": 1.6, "warmupSpeed": 0.015, "blockedItem": None, "drawMineItem": True, "drillEffect": "mine", "drillEffectRnd": -1.0, "rotateSpeed": 2.0, "updateEffect": "pulverizeSmall", "updateEffectChance": 0.02, "drawRim": False, "drawSpinSprite": True, "heatColor": "ff5512ff", "rimRegion": None, "rotatorRegion": None, "topRegion": None, "itemRegion": None},
			"BurstDrill": {"extend": "Drill", "shake": 2.0, "speedCurve": "pow2In", "topInvertRegion": None, "glowRegion": None, "arrowRegion": None, "arrowBlurRegion": None, "invertedTime": 200.0, "arrowSpacing": 4.0, "arrowOffset": 0.0, "arrows": 3, "arrowColor": "feb380ff", "baseArrowColor": "6e7080ff", "glowColor": "feb380ff"},
		"DroneCenter": {"extend": "Block", "unitsSpawned": 4, "droneType": None, "status": "overdrive", "droneConstructTime": 180.0, "statusDuration": 120.0, "droneRange": 50.0},
		"HeatConductor": {"extend": "Block", "visualMaxHeat": 15.0, "drawer": None},
		"Junction": {"extend": "Block", "speed": 26.0, "capacity": 6},
		"ItemBridge": {"extend": "Block", "timerCheckMoved": 1, "range": 0, "transportTime": 2.0, "endRegion": None, "bridgeRegion": None, "arrowRegion": None, "fadeIn": True, "moveArrows": True, "pulse": False, "arrowSpacing": 4.0, "arrowOffset": 2.0, "arrowPeriod": 0.4, "arrowTimeScl": 6.2, "lastBuild": None},
			"LiquidBridge": {"extend": "ItemBridge"},
			"BufferedItemBridge": {"extend": "ItemBridge", "timerAccept": 2, "speed": 40.0, "bufferCapacity": 50},
		"LiquidVoid": {"extend": "Block"},
		"MassDriver": {"extend": "Block", "range": 0.0, "rotateSpeed": 5.0, "translation": 7.0, "minDistribute": 10, "knockback": 4.0, "reload": 100.0, "bullet": None, "bulletSpeed": 5.5, "bulletLifetime": 200.0, "shootEffect": "shootBig2", "smokeEffect": "shootBigSmoke2", "receiveEffect": "mineBig", "shootSound": "shootBig", "shake": 3.0, "baseRegion": None},
		"MemoryBlock": {"extend": "Block", "memoryCapacity": 32},
		"MendProjector": {"extend": "Block", "timerUse": 1, "baseColor": "84f491ff", "phaseColor": "84f491ff", "topRegion": None, "reload": 250.0, "range": 60.0, "healPercent": 12.0, "phaseBoost": 12.0, "phaseRangeBoost": 50.0, "useTime": 400.0},
		"PayloadBlock": {"extend": "Block", "payloadSpeed": 0.7, "payloadRotateSpeed": 5.0, "regionSuffix": "", "topRegion": None, "outRegion": None, "inRegion": None},
			"PayloadMassDriver": {"extend": "PayloadBlock", "range": 100.0, "rotateSpeed": 2.0, "length": 11.125, "knockback": 5.0, "reload": 30.0, "chargeTime": 100.0, "maxPayloadSize": 3.0, "grabWidth": 8.0, "grabHeight": 2.75, "shootEffect": "shootBig2", "smokeEffect": "shootPayloadDriver", "receiveEffect": "payloadReceive", "shootSound": "shootBig", "shake": 3.0, "transferEffect": "flyingUnitLow - 1)", "baseRegion": None, "capRegion": None, "leftRegion": None, "rightRegion": None, "capOutlineRegion": None, "leftOutlineRegion": None, "rightOutlineRegion": None, "arrow": None},
			"PayloadVoid": {"extend": "PayloadBlock", "incinerateEffect": "blastExplosion", "incinerateSound": "bang"},
			"PayloadSource": {"extend": "PayloadBlock"},
			"UnitBlock": {"extend": "PayloadBlock"},
				"Reconstructor": {"extend": "UnitBlock", "constructTime": 120.0, "upgrades": None, "capacities": []},
		"PowerBlock": {"extend": "Block"},
			"PayloadDeconstructor": {"extend": "PowerBlock", "maxPayloadSize": 4.0, "deconstructSpeed": 2.5, "dumpRate": 4},
			"PayloadLoader": {"extend": "PowerBlock", "timerLoad": 1, "loadTime": 2.0, "itemsLoaded": 8, "liquidsLoaded": 40.0, "maxBlockSize": 3, "maxPowerConsumption": 40.0, "loadPowerDynamic": True},
				"PayloadUnloader": {"extend": "PayloadLoader", "offloadSpeed": 4, "maxPowerUnload": 80.0},
			"PowerNode": {"extend": "PowerBlock", "laser": None, "laserEnd": None, "laserRange": 6.0, "maxNodes": 3, "autolink": True, "drawRange": True, "laserScale": 0.25, "laserColor1": "ffffffff", "laserColor2": "fbd367ff"},
				"LongPowerNode": {"extend": "PowerNode", "glow": None, "glowColor": "cbfd8172", "glowScl": 16.0, "glowMag": 0.6},
				"PowerSource": {"extend": "PowerNode", "powerProduction": 10000.0},
			"PowerVoid": {"extend": "PowerBlock"},
			"PowerDistributor": {"extend": "PowerBlock"},
				"Battery": {"extend": "PowerDistributor", "topRegion": None, "emptyLightColor": "f8c266ff", "fullLightColor": "fb9567ff"},
				"PowerGenerator": {"extend": "PowerDistributor", "powerProduction": 0.0, "generationType": "basePowerGeneration", "drawer": None},
					"ConsumeGenerator": {"extend": "PowerGenerator", "itemDuration": 120.0, "effectChance": 0.01, "generateEffect": None, "consumeEffect": None, "generateEffectRange": 3.0, "liquidOutput": None, "filterItem": None, "filterLiquid": None},
					"ImpactReactor": {"extend": "PowerGenerator", "timerUse": 1, "warmupSpeed": 0.001, "itemDuration": 60.0, "explosionRadius": 23, "explosionDamage": 1900, "explodeEffect": "impactReactorExplosion", "plasma1": "ffd06bff", "plasma2": "ff361bff", "bottomRegion": None, "plasmaRegions": None},
					"NuclearReactor": {"extend": "PowerGenerator", "timerFuel": 1, "tr": None, "lightColor": "7f19eaff", "coolColor": "ffffff00", "hotColor": "ff9575a3", "explodeEffect": "reactorExplosion", "itemDuration": 120.0, "heating": 0.01, "smokeThreshold": 0.3, "flashThreshold": 0.46, "explosionRadius": 19, "explosionDamage": 1250, "coolantPower": 0.5, "smoothLight": 0.0, "fuelItem": "thorium", "topRegion": None, "lightsRegion": None},
				"BeamNode": {"extend": "PowerBlock", "range": 5, "laser": None, "laserEnd": None, "laserColor1": "ffffffff", "laserColor2": "ffd9c2ff", "pulseScl": 7.0, "pulseMag": 0.05, "laserWidth": 0.4},
		"BeamDrill": {"extend": "Block", "laser": None, "laserEnd": None, "laserCenter": None, "laserBoost": None, "laserEndBoost": None, "laserCenterBoost": None, "topRegion": None, "glowRegion": None, "drillTime": 200.0, "range": 5, "tier": 1, "laserWidth": 0.65, "optionalBoostIntensity": 2.5, "sparkColor": "fd9e81ff", "glowColor": "ffffffff", "glowIntensity": 0.2, "pulseIntensity": 0.07, "glowScl": 3.0, "sparks": 7, "sparkRange": 10.0, "sparkLife": 27.0, "sparkRecurrence": 4.0, "sparkSpread": 45.0, "sparkSize": 3.5, "boostHeatColor": "75b3ccff", "heatColor": "ff5959e5", "heatPulse": 0.3, "heatPulseScl": 7.0},
		"CanvasBlock": {"extend": "Block", "padding": 0.0, "canvasSize": 8, "palette": [0x634b7dff, 0xc45d9f_ff, 0xe39aac_ff, 0xf0dab1_ff, 0x6461c2_ff, 0x2ba9b4_ff, 0x93d4b5_ff, 0xf0f6e8_ff], "bitsPerPixel": 0, "colorToIndex": None},
		"Cliff": {"extend": "Block", "size": 11.0, "cliffs": None, "editorCliffs": None},

		"BaseTurret": {"extend": "Block", "range": 80.0, "placeOverlapMargin": 56.0, "rotateSpeed": 5.0, "coolEffect": "fuelburn", "coolantMultiplier": 5.0, "coolant": None},
			"ReloadTurret": {"extend": "BaseTurret", "reload": 10.0},
				"PointDefenseTurret": {"extend": "ReloadTurret", "timerTarget": 1, "retargetTime": 5.0, "baseRegion": None, "color": "ffffffff", "beamEffect": "pointBeam", "hitEffect": "pointHit", "shootEffect": "sparkShoot", "shootSound": "lasershoot", "shootCone": 5.0, "bulletDamage": 10.0, "shootLength": 3.0},
				"Turret": {"extend": "ReloadTurret", "timerTarget": 1, "targetInterval": 20.0, "maxAmmo": 30, "ammoPerShot": 1, "consumeAmmoOnce": True, "heatRequirement": -1.0, "maxHeatEfficiency": 3.0, "inaccuracy": 0.0, "velocityRnd": 0.0, "shootCone": 8.0, "shootX": 0.0, "shootY": None, "xRand": None, "minRange": 0.0, "minWarmup": 0.0, "accurateDelay": True, "moveWhileCharging": True, "shoot": None, "targetAir": True, "targetGround": True, "targetHealing": False, "playerControllable": True, "displayAmmoMultiplier": True, "unitSort": "closest", "unitFilter": ["code"], "buildingFilter": "underBullets", "heatColor": "ab3400ff", "shootEffect": None, "smokeEffect": None, "ammoUseEffect": None, "shootSound": "shoot", "chargeSound": None, "soundPitchMin": 0.9, "soundPitchMax": 1.1, "ammoEjectBack": 1.0, "shootWarmupSpeed": 0.1, "linearWarmup": False, "recoil": 1.0, "recoilTime": -1.0, "recoilPow": 1.8, "cooldownTime": 20.0, "elevation": -1.0, "shake": 0.0, "drawer": None},
					"PayloadAmmoTurret": {"extend": "Turret", "ammoTypes": None},
					"ContinuousTurret": {"extend": "Turret", "shootType": "placeholder"},
						"ContinuousLiquidTurret": {"extend": "ContinuousTurret", "ammoTypes": None, "liquidConsumed": 0.016666668},
					"ItemTurret": {"extend": "Turret", "ammoTypes": None},
					"LiquidTurret": {"extend": "Turret", "ammoTypes": None, "extinguish": True},
					"PowerTurret": {"extend": "Turret", "shootType": None},
						"LaserTurret": {"extend": "PowerTurret", "firingMoveFract": 0.25, "shootDuration": 100.0},
		"DirectionBridge": {"extend": "Block", "bridgeRegion": None, "bridgeBotRegion": None, "bridgeLiquidRegion": None, "arrowRegion": None, "dirRegion": None, "range": 4},
			"DirectionLiquidBridge": {"extend": "DirectionBridge", "timerFlow": 1, "speed": 5.0, "liquidPadding": 1.0, "bottomRegion": None},
			"DuctBridge": {"extend": "DirectionBridge", "speed": 5.0},
		"DirectionalForceProjector": {"extend": "Block", "width": 30.0, "shieldHealth": 3000.0, "cooldownNormal": 1.75, "cooldownLiquid": 1.5, "cooldownBrokenBase": 0.35, "absorbEffect": "absorb", "shieldBreakEffect": "shieldBreak", "topRegion": None, "length": 40.0, "padSize": 40.0},
		"DirectionalUnloader": {"extend": "Block", "centerRegion": None, "topRegion": None, "arrowRegion": None, "speed": 1.0, "allowCoreUnload": False},

		"Duct": {"extend": "Block", "speed": 5.0, "armored": False, "transparentColor": "66666619", "topRegions": None, "botRegions": None},
		"DuctRouter": {"extend": "Block", "speed": 5.0, "topRegion": None},

		"ForceProjector": {"extend": "Block", "timerUse": 1, "phaseUseTime": 350.0, "phaseRadiusBoost": 80.0, "phaseShieldBoost": 400.0, "radius": 101.7, "shieldHealth": 700.0, "cooldownNormal": 1.75, "cooldownLiquid": 1.5, "cooldownBrokenBase": 0.35, "coolantConsumption": 0.1, "consumeCoolant": True, "absorbEffect": "absorb", "shieldBreakEffect": "shieldBreak", "topRegion": None, "itemConsumer": None, "coolantConsumer": None},

		"Incinerator": {"extend": "Block", "effect": "fuelburn", "flameColor": "ffad9dff"},
		"ItemIncinerator": {"extend": "Block", "effect": "incinerateSlag", "effectChance": 0.2, "liquidRegion": None, "topRegion": None},
		"ItemSource": {"extend": "Block", "itemsPerSecond": 100},
		"ItemVoid": {"extend": "Block"},
		"LaunchPad": {"extend": "Block", "launchTime": 1.0, "launchSound": None, "lightRegion": None, "podRegion": None, "lightColor": "eab678ff"},

		"LightBlock": {"extend": "Block", "brightness": 0.9, "radius": 200.0, "topRegion": None},

		"LiquidSource": {"extend": "Block", "crossRegion": None, "bottomRegion": None},
		"LogicBlock": {"extend": "Block", "maxInstructionScale": 5, "instructionsPerTick": 1, "maxInstructionsPerTick": 40, "range": 80.0},
		"LogicDisplay": {"extend": "Block", "maxSides": 25, "displaySize": 64, "scaleFactor": 1.0},
		"MessageBlock": {"extend": "Block", "maxTextLength": 220, "maxNewlines": 24},

		"OverdriveProjector": {"extend": "Block", "timerUse": 1, "topRegion": None, "reload": 60.0, "range": 80.0, "speedBoost": 1.5, "speedBoostPhase": 0.75, "useTime": 400.0, "phaseRangeBoost": 20.0, "hasBoost": True, "baseColor": "feb380ff", "phaseColor": "ffd59eff"},
		"OverflowDuct": {"extend": "Block", "speed": 5.0, "topRegion": None},
		"OverflowGate": {"extend": "Block", "speed": 1.0, "invert": False},

		"PayloadConveyor": {"extend": "Block", "moveTime": 45.0, "moveForce": 201.0, "topRegion": None, "edgeRegion": None, "interp": "pow5", "payloadLimit": 3.0},
			"PayloadRouter": {"extend": "PayloadConveyor", "overRegion": None},

		"PowerDiode": {"extend": "Block", "arrow": None},
		"Prop": {"extend": "Block"},

		"Radar": {"extend": "Block", "discoveryTime": 600.0, "rotateSpeed": 2.0, "baseRegion": None, "glowRegion": None, "glowColor": "ab3400ff", "glowScl": 5.0, "glowMag": 0.6},
		"RegenProjector": {"extend": "Block", "range": 14, "healPercent": 0.2, "optionalMultiplier": 2.0, "optionalUseTime": 480.0, "drawer": None, "effectChance": 0.03, "baseColor": "ffd37fff", "effect": "regenParticle"},
		"RepairTower": {"extend": "Block", "range": 80.0, "circleColor": "98ffa9ff", "glowColor": "98ffa97f", "circleSpeed": 120.0, "circleStroke": 3.0, "squareRad": 3.0, "squareSpinScl": 0.8, "glowMag": 0.5, "glowScl": 8.0, "healAmount": 1.0, "glow": None},
		"RepairTurret": {"extend": "Block", "timerTarget": 1, "timerEffect": 2, "repairRadius": 50.0, "repairSpeed": 0.3, "powerUse": 0.0, "length": 5.0, "beamWidth": 1.0, "pulseRadius": 6.0, "pulseStroke": 2.0, "acceptCoolant": False, "coolantUse": 0.5, "coolEffect": "fuelburn", "coolantMultiplier": 1.0, "baseRegion": None, "laser": None, "laserEnd": None, "laserTop": None, "laserTopEnd": None, "laserColor": "98ffa9ff", "laserTopColor": "ffffffff"},

		"Router": {"extend": "Block", "speed": 8.0},

		"Prop": {"extend": "Block"},
			"Seaweed": {"extend": "Prop"},
			"SeaBush": {"extend": "Prop", "botRegion": None, "centerRegion": None, "lobesMin": 7, "lobesMax": 7, "botAngle": 60.0, "origin": 0.1, "sclMin": 30.0, "sclMax": 50.0, "magMin": 5.0, "magMax": 15.0, "timeRange": 40.0, "spread": 0.0},

		"Separator": {"extend": "Block", "results": None, "craftTime": 0.0, "liquidRegion": None, "spinnerRegion": None, "spinnerSpeed": 3.0},
		"ShieldBreaker": {"extend": "Block", "toDestroy": [], "effect": "shockwave", "breakEffect": "reactorExplosion", "selfKillEffect": "massiveExplosion"},
		#"ShockMine": {"extend": "Block", "timerDamage": 1, "cooldown": 80.0},


			#"genericsmelter": {"type": "GenericSmelter", "name": "Name", "description": "Description", "health": "120", "size": "1", "requirements": [{ "item": "lead", "amount": 2}], "hasPower": False, "hasItems": False, "hasLiquids": False, "craftTime": "3", "consumes": "{}", "updateEffect": "", "category": "crafting", "research": "cultivator", "alwaysUnlocked": False, "idleSoundVolume": 1.5, "itemCapacity": 30, "outputLiquid": {}},
		
	
	#"items": {
	#	"items": {"name": "Name", "description": "Description", "color": "000000ff", "explosiveness": 0.0, "fliammbility": 0.0, "radiioactivity": 0.0, "hardness": 0, "cost": 1.0, "healthScaling": 0.0, "lowPriority": False, "frames": 0, "transitionFrames": 0, "frameTime": 5.0, "buildable": True, "research": "copper", "alwaysUnlocked": False},
			
	#	"material": {"type": "Material", "name": "Name", "description": "Description", "color": "000000ff", "explosiveness": 0.0, "fliammbility": 0.0, "radiioactivity": 0.0, "hardness": 0, "cost": 1.0, "healthScaling": 0.0, "lowPriority": False, "frames": 0, "transitionFrames": 0, "frameTime": 5.0, "buildable": True, "research": "copper", "alwaysUnlocked": False},
	#	"resource": {"type": "Resource", "name": "Name", "description": "Description", "color": "000000ff", "explosiveness": 0.0, "fliammbility": 0.0, "radiioactivity": 0.0, "hardness": 0, "cost": 1.0, "healthScaling": 0.0, "lowPriority": False, "frames": 0, "transitionFrames": 0, "frameTime": 5.0, "buildable": True, "research": "copper", "alwaysUnlocked": False},
	#},

	#"liquids": {
	#	"liquids": {"name": "Name", "description": "Description", "color": "ffffff", "explosiveness": "0", "fliammbility": "0", "radioactivity": "0", "hardness": "1", "cost": "1", "viscosity": "0.55", "heatCapacity": "3", "effect": "freezing", "lightColor": "000000", "research": "copper", "alwaysUnlocked": False},
			
	#	"liquid": {"name": "Name", "description": "Description", "color": "ffffff", "explosiveness": "0", "fliammbility": "0", "radioactivity": "0", "hardness": "1", "cost": "1", "viscosity": "0.55", "heatCapacity": "3", "effect": "freezing", "lightColor": "000000", "research": "copper", "alwaysUnlocked": False},
	#}
	}


def pillowToPixmap(pillowImage):
	try:
		pillowImage.convert("RGBA")
		return QtGui.QPixmap().fromImage(ImageQt(pillowImage))
	except:
		try:
			pillowImage_data = pillowImage.convert("RGBA").tobytes("raw", "RGBA")
			img = QtGui.QImage(pillowImage_data, pillowImage.size[0], pillowImage.size[1],
							   QtGui.QImage.Format.Format_RGBA8888)
			return QtGui.QPixmap.fromImage(img)
		except:
			return QtGui.QPixmap("\\resources\\icons\\error.png")

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setBaseSize(800, 700)
		self.setMinimumSize(800, 700)
		self.setWindowTitle("Mindustry Mod Construct")
		self.setStyleSheet("background-color: #252525;")
		self.setAcceptDrops(True)



	'''def dragEnterEvent(self, event):
		if event.mimeData().hasUrls():
			event.accept()
		else:
			event.ignore()

	def dropEvent(self, event):
		files = [u.toLocalFile() for u in event.mimeData().urls()]
		for f in files:
			print(f)'''
class DrawWindow(QFrame):
	def TimerUpdate(self):
		
		if self.attachedWidget != None:
			if self.attachedWidget.parentWidget() != window:
				self.move(self.attachedWidget.x() + self.attachedWidget.parentWidget().x(), self.attachedWidget.y() + self.attachedWidget.parentWidget().y())
				self.resize(self.attachedWidget.width(), self.attachedWidget.height())
			else:
				self.move(self.attachedWidget.x(), self.attachedWidget.y())
				self.resize(self.attachedWidget.width(), self.attachedWidget.height())

			self.allUpdate()
	
	def mouseDoubleClickEvent(self, event):
		self.attach()
	def setBaseGeometry(self, _x, _y, _width, _height):
		self.baseGeometry = QRect(_x, _y, _width, _height)
	def __init__(self):
		super().__init__(window, objectName="window")
		self.move(300, 300)
		self.resize(300, 300)
		self.setMinimumSize(300, 300)
		
		self.setBaseGeometry(300, 300, 300, 300)


		#self.setWindowTitle("Test")
		self.setStyleSheet("QFrame#window { background-color:#252525; border-style: solid; border-width: 3px; border-color: #454545; } color: #ffffff; QLabel { background-color: #00000000; border-width: 0px }")
		self.setProperty("class", "window")
		#self.setAcceptDrops(True)


		self.attachedWidget = None

		main = self

		self.timerUpdate = QTimer()
		self.timerUpdate.setInterval(100)
		self.timerUpdate.timeout.connect(self.TimerUpdate)
		self.timerUpdate.start()

		class UpPanel(QFrame):

			

			def __init__(self):
				super().__init__(window, objectName="window")
				self.panelHeight = 25
				self.move(main.x(), main.y() - self.panelHeight)
				self.resize(main.width(), self.panelHeight)
				self.setStyleSheet("QFrame#window { background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; }  ")
				self.mi = False
				self.mx = 0
				self.my = 0

				self.isAttached = False

				self.title = QLabel(self)
				self.title.move(5, 3)
				self.title.resize(self.width() - 100, self.height() - 6)
				self.title.setStyleSheet( "background-color:#000000; color: #ffffff; border-width: 0px; font-size: 10; font-family: fontello" )
				self.title.setText("Тест")
				
				self.buttonClose = QPushButton(self)
				self.buttonClose.move(self.width()-self.panelHeight, 0)
				self.buttonClose.resize(self.panelHeight, self.panelHeight)
				self.buttonClose.setStyleSheet(StyleSheetList[0])
				self.buttonClose.clicked.connect(self.closeWindow)
				self.buttonClose.setText("")
				#self.buttonClose.hide()
				
				self.buttonHide = QPushButton(self)
				self.buttonHide.move(self.width()-(self.panelHeight*2), 0)
				self.buttonHide.resize(self.panelHeight, self.panelHeight)
				self.buttonHide.setStyleSheet(StyleSheetList[0])
				self.buttonHide.clicked.connect(self.hideWindow)
				self.buttonHide.setText("") #

				#self.openWindow()
			
				self.titleBarHeight = app.style().pixelMetric(
					QStyle.PixelMetric.PM_TitleBarHeight,
					QStyleOptionTitleBar(),
					window
				)

			def setTitle(self, _text):
				self.title.setText(_text)

			def openWindow(self):


				main.show()
				self.show()

				main.raise_()
				self.raise_()

			def closeWindow(self):
				main.attach()

				main.hide()
				self.hide()

			
			
			def hideWindow(self):
				if main.isHidden():
					main.show()
					self.buttonHide.setText("") #
				else:
					main.hide()
					self.buttonHide.setText("") #
			def mouveButtons(self):
				self.buttonClose.move(self.width()-(self.panelHeight*1), 0)
				self.buttonHide.move(self.width()-(self.panelHeight*2), 0)

			def mousePressEvent(self, event):
				if self.mi == False:
					self.mi = True
					self.mx = self.x() - QtGui.QCursor.pos().x()
					self.my = self.y() - QtGui.QCursor.pos().y()

				main.raise_()
				self.raise_()
			def mouseReleaseEvent(self, event):
				self.mi = False
				main.move(int(QtGui.QCursor.pos().x() + self.mx), int(QtGui.QCursor.pos().y() + self.my + self.panelHeight))
				self.move(int(QtGui.QCursor.pos().x() + self.mx), int(QtGui.QCursor.pos().y() + self.my))

				if main.attachedWidget == None:
					for i in attachebleWidgets:
						if i.attachedWidget == None:
							if QtGui.QCursor.pos().x() - window.x() > i.x() and QtGui.QCursor.pos().x() - window.x() < i.x() + i.width():
								if QtGui.QCursor.pos().y() - window.y() - self.titleBarHeight > i.y() and QtGui.QCursor.pos().y() - window.y() - self.titleBarHeight < i.y() + i.height():
									main.attach(i)
			def mouseMoveEvent(self, event):
				if self.mi:
					main.move(int(QtGui.QCursor.pos().x() + self.mx), int(QtGui.QCursor.pos().y() + self.my + self.panelHeight))
					self.move(int(QtGui.QCursor.pos().x() + self.mx), int(QtGui.QCursor.pos().y() + self.my))

					

					if main.attachedWidget == None:
						for i in attachebleWidgets:
							i.setStyleSheet("border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff")
							if i.attachedWidget == None:
								if QtGui.QCursor.pos().x() - window.x() > i.x() and QtGui.QCursor.pos().x() - window.x() < i.x() + i.width():
									if QtGui.QCursor.pos().y() - window.y() - self.titleBarHeight > i.y() and QtGui.QCursor.pos().y() - window.y() - self.titleBarHeight < i.y() + i.height():
										i.setStyleSheet("border-style: dashed; border-width: 3px; border-color: #ffd37f; color: #ffffff")

		upPanel = UpPanel()
		self.upPanel = upPanel

		class FrameResizer_R(QFrame):
			def __init__(self):
				super().__init__(main)
				self.move(main.width() - 3, 0)
				self.resize(3, main.height())

				self.setStyleSheet(" QFrame { background-color: #454545 } QFrame:hover { background-color: #ffd37f }")
				self.mi = False



			def update(self):
				self.move(min(max(int(QtGui.QCursor.pos().x() - window.x() - main.x()), main.minimumWidth()), main.maximumWidth()) - 3, 0)
				main.resize(self.x() + 3, main.height())

				main.allUpdate()


			def mousePressEvent(self, event):
				if self.mi == False:
					self.mi = True
			def mouseReleaseEvent(self, event):
				self.mi = False
				self.mx = 0

				self.update()
				self.move(main.width() - 3, 0)
			def mouseMoveEvent(self, event):
				if self.mi:
					self.update()
					
		class FrameResizer_D(QFrame):
			def __init__(self):
				super().__init__(main)
				self.move(0, main.height() - 3)
				self.resize(main.width(), 3)

				self.setStyleSheet(" QFrame { background-color: #454545 } QFrame:hover { background-color: #ffd37f }")
				self.mi = False

			def update(self):
				self.move(0, int(min(max(QtGui.QCursor.pos().y() - window.y() - main.y() - upPanel.panelHeight, main.minimumHeight()), main.maximumHeight())))
				main.resize(main.width(), self.y() + 3)

				main.allUpdate()

			def mousePressEvent(self, event):
				if self.mi == False:
					self.mi = True
			def mouseReleaseEvent(self, event):
				self.mi = False

				self.update()
				self.move(0, main.height() - 3)
			def mouseMoveEvent(self, event):
				if self.mi:
					self.update()
					
		class FrameResizer_L(QFrame):
			def __init__(self):
				super().__init__(main)
				self.move(0, 0)
				self.resize(3, main.height())

				self.setStyleSheet(" QFrame { background-color: #454545 } QFrame:hover { background-color: #ffd37f }")
				self.mi = False
				self.mx = 0
				self.mx2 = 0

			def update(self):
				self.move(0, 0)
				if main.width() <= main.minimumWidth():
					pass
				else:
					main.move(QtGui.QCursor.pos().x() - window.x(), main.y())

				
				
				main.resize( self.mx - (QtGui.QCursor.pos().x() - window.x()) + self.mx2, main.height())
				
				main.allUpdate()

				

			def mousePressEvent(self, event):
				if self.mi == False:
					self.mi = True
					self.mx = QtGui.QCursor.pos().x() - window.x()
					self.mx2 = main.width()

			def mouseReleaseEvent(self, event):
				self.mi = False

				self.update()
				self.move(0, 0)
			def mouseMoveEvent(self, event):
				if self.mi:
					self.update()

					
		
					

		self.R = FrameResizer_R()
		self.L = FrameResizer_L()
		self.D = FrameResizer_D()

	def allUpdate(self):
		self.upPanel.move(self.x(), self.y() - self.upPanel.panelHeight)
		self.upPanel.resize(self.width(), self.upPanel.panelHeight)
		self.upPanel.mouveButtons()

		self.R.move(self.width() - self.R.width(), 0)
		self.R.resize(self.R.width(), self.height())
		
		self.L.move(0, 0)
		self.L.resize(self.R.width(), self.height())
		
		self.D.move(0, self.height() - self.D.height())
		self.D.resize(self.width(), self.D.height())

	def attach(self, _widget = None):
		#print(type(_widget))
		#print(hasattr(_widget, 'x'))
		self.upPanel.mx = 0

		if hasattr(_widget, 'x'):
			self.attach()

			self.attachedWidget = _widget
			self.attachedWidget.attachedWidget = self

			self.attachedWidget.setStyleSheet("border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff")

			#self.attachedWidget.setBaseGeometry(self.attachedWidget.geometry)
			
			#self.attachedWidget.resize(self.size())


			self.show()

			print(self.attachedWidget)

			self.upPanel.hide()

			self.L.hide()
			self.R.hide()
			self.D.hide()

		else:
			try:
				self.attachedWidget.attachedWidget = None
				#self.attachedWidget.setGeometry(self.attachedWidget.baseGeometry())
			except Exception as x:
				print("op: " + str(x))
			
			

			self.attachedWidget = None

			

			#self.setParent(window)
			#upPanel.setParent(window)

			self.upPanel.show()

			self.L.show()
			self.R.show()
			self.D.show()

			

		

		
		
		
	def mousePressEvent(self, event):
		self.raise_()
		self.upPanel.raise_()
		

#qApp.shutdown()
app = QApplication(sys.argv)

window = MainWindow()






id = QFontDatabase.addApplicationFont("resources\\font.ttf")
if id < 0: 
	print("Error")
families = QFontDatabase.applicationFontFamilies(id)
print(families[0])





def zip_directory(folder_path, zip_path):
	print(folder_path)
	print(zip_path)
	shutil.make_archive(zip_path, 'zip', folder_path)

def coloritaText(text):
	i = 0
	i2 = 0
	i3 = 0
	itext = ""

	#ModVer.setText('<font color="blue">' + str(RootMod[0]["version"]) + '</font>')

	for it in text:
		if it != "[" and it != "]":
			itext += it
		if it == "[" and i == 0:
			i += 1
			itext += '<font color="'
		if it == "]" and i == 1:
			itext += '">'
			i -= 1
	print(itext)
	return itext



def getSuffixPath(_path):
	return Path(_path).suffixes[0][1:]
	

def toPng(text, endAdd = ""):
	if text[-5:] == ".json":
		text1 = text[:-5]
		text1 += endAdd + ".png"
	if text[-6:] == ".hjson":
		text1 = text[:-6]
		text1 += endAdd + ".png"
	return text1
buferMessage = []
def SummonMessage(_text, _them = "message", _window = window):
	_tempp = QLabel(_window)

	_tempp.setText(str(_text))
	_tempp.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

	if _them == "error":
		_tempp.setStyleSheet("background-color: rgba(0, 0, 0, 135); border-color: #e55454; border-width: 2 px; border-style: solid ; color: #ffffff")
	else:
		_tempp.setStyleSheet("background-color: rgba(0, 0, 0, 135); border-color: #ffd37f; border-width: 2 px; border-style: solid ; color: #ffffff")
	_tempp.setFont(QFont(families[0], 12))
	_tempp.move(0, 0)

	

	_tempp.adjustSize()
	_tempp.resize(_tempp.width() + 15, _tempp.height() + 15)
	_tempp.show()

	if _them == "info":
		_tempp.move(0, (_tempp.height() * -1))

	for i in buferMessage:
		if _tempp.y() + _tempp.height() > i["widget"].y() and i["window"] == _window:
			i["widget"].move(int(i["window"].width()/2 - i["widget"].width()/2), i["widget"].y() + _tempp.height())

	buferMessage.append({"widget": _tempp, "them": _them, "window": _window})

	print("[SummonMessage]: " + str(_text))
def openFiler(pathF):
	try:
		_text = None
		with open(pathF, 'r') as f:
			_text = f.read()

		_tempCon = ""

		for o in _text:
			if o == "'":
				_tempCon += '"'
			else:
				_tempCon += o
			
			

		data = None

		if getSuffixPath(pathF) == "json":
			#data = json.loads(_tempCon)
			#print("json")
			try:
				data = json.loads(_tempCon)
			except Exception:
				try:
					data = hjson.loads(_tempCon)
				except Exception:
					try:
						data = json.loads(_text)
					except Exception:
						data = hjson.loads(_text)
		if getSuffixPath(pathF) == "hjson":
			#data = hjson.loads(_tempCon)
			try:
				data = hjson.loads(_tempCon)
			except Exception:
				try:
					data = hjson.loads(_text)
				except Exception:
					pass
					#try:
					#	data = json.load(f)
					#except JSONDecodeError:
					#	data = json.loads(_tempCon)
		if data == {}:
			try:
				data = json.loads(_tempCon)
			except Exception:
				data = hjson.loads(_tempCon)
		
		opsa = [data, _text]
			
	except JSONDecodeError:
		opsa = [None, _text]
		SummonMessage("Json Файл не получаетса Открыть", "error")
	except HjsonDecodeError:
		opsa = [None, _text]
		SummonMessage("Hjson Файл не получаетса Открыть", "error")
	except Exception as x:
		opsa = [None, _text]
		SummonMessage(x, "error")
	print(opsa)
	return opsa

ContentL = []
ContentL1 = []
	
SpriteL = []

DefaultFileSave = {
		"mod": {"name": "Name", "displayName": "DisplayName", "description": "Description", "author": "Author", "version": "0.1", "minGameVersion": "105", "dependencies": [], "hidden": False},
		"blocks": {
			"wall": {"type": "Wall", "name": "Name", "description": "Description", "health": "120", "size": "1", "requirements": "[]", "category": "defense", "research": "copper-wall", "alwaysUnlocked": False},
			"conveyor": {"type": "Conveyor", "name": "Name", "description": "Description", "health": "120", "speed": "1", "itemCapacity": 30, "requirements": "[]", "category": "distribution", "research": "copper-wall", "alwaysUnlocked": False},
			"conduit": {"type": "Conduit", "name": "Exmii", "description": "Description", "health": "120", "speed": "1", "Liquid Capacity": 10, "requirements": "[]", "category": "distribution", "research": "copper-wall", "alwaysUnlocked": False},
			"drill": {"type": "Drill", "name": "Drill", "description": "Description", "health": "120", "speed": "1", "tier": 2, "drillTime": 300, "drillEffect": "mine", "requirements": "[]", "consumes": "{}", "category": "production", "research": "copper-wall", "alwaysUnlocked": False},
			
			"genericcrafter": {"type": "GenericCrafter", "name": "Name", "description": "Description", "health": "120", "size": "1", "requirements": [{ "item": "lead", "amount": 2}], "hasPower": False, "hasItems": False, "hasLiquids": False, "craftTime": "3", "consumes": "{}", "updateEffect": "", "category": "crafting", "research": "cultivator", "alwaysUnlocked": False, "idleSoundVolume": 1.5, "itemCapacity": 30, "outputItem": { "item": "Copper", "amount": 1}},
			"genericsmelter": {"type": "GenericSmelter", "name": "Name", "description": "Description", "health": "120", "size": "1", "requirements": [{ "item": "lead", "amount": 2}], "hasPower": False, "hasItems": False, "hasLiquids": False, "craftTime": "3", "consumes": "{}", "updateEffect": "", "category": "crafting", "research": "cultivator", "alwaysUnlocked": False, "idleSoundVolume": 1.5, "itemCapacity": 30, "outputLiquid": {}},
		
		},
		"items": {
			"items": {"name": "Name", "description": "Description", "color": "000000ff", "explosiveness": 0.0, "fliammbility": 0.0, "radiioactivity": 0.0, "hardness": 0, "cost": 1.0, "healthScaling": 0.0, "lowPriority": False, "frames": 0, "transitionFrames": 0, "frameTime": 5.0, "buildable": True, "research": "copper", "alwaysUnlocked": False},
			
			"material": {"type": "Material", "name": "Name", "description": "Description", "color": "000000ff", "explosiveness": 0.0, "fliammbility": 0.0, "radiioactivity": 0.0, "hardness": 0, "cost": 1.0, "healthScaling": 0.0, "lowPriority": False, "frames": 0, "transitionFrames": 0, "frameTime": 5.0, "buildable": True, "research": "copper", "alwaysUnlocked": False},
			"resource": {"type": "Resource", "name": "Name", "description": "Description", "color": "000000ff", "explosiveness": 0.0, "fliammbility": 0.0, "radiioactivity": 0.0, "hardness": 0, "cost": 1.0, "healthScaling": 0.0, "lowPriority": False, "frames": 0, "transitionFrames": 0, "frameTime": 5.0, "buildable": True, "research": "copper", "alwaysUnlocked": False},
		},

		"liquids": {
			"liquids": {"name": "Name", "description": "Description", "color": "ffffff", "explosiveness": "0", "fliammbility": "0", "radioactivity": "0", "hardness": "1", "cost": "1", "viscosity": "0.55", "heatCapacity": "3", "effect": "freezing", "lightColor": "000000", "research": "copper", "alwaysUnlocked": False},
			
			"liquid": {"name": "Name", "description": "Description", "color": "ffffff", "explosiveness": "0", "fliammbility": "0", "radioactivity": "0", "hardness": "1", "cost": "1", "viscosity": "0.55", "heatCapacity": "3", "effect": "freezing", "lightColor": "000000", "research": "copper", "alwaysUnlocked": False},
			
			
		},
		
		#"nuclearreactor": {"type": "NuclearReactor", "name": "Exmii", "description": "Description", "health": "120", "size": "1", "heating": 0.02, "requirements": [{ "item": "lead", "amount": 2}], "hasPower": False, "hasItems": False, "hasLiquids": False, "craftTime": "3", "consumes": "{}", "updateEffect": "teleportActivate", "category": "power", "research": "thorium-reactor", "itemCapacity": 30, "powerProduction": 71, "itemDuration" : 170, "idleSoundVolume": 1.5},

		
		}
'''
def setThem(_widget = None, color = "#ffffff", background_color = "#000000", border = [3, "solid", "#454545"], color_hover = "#ffffff", background_color_hover = "#000000", border_hover = [3, "solid", "#ffd37f"]):
	print(type(_widget))
	#_temp = "QPushButton { background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover { background-color:#000000; border-style: solid; border-width: 3px; border-color: #ffd37f; color: #ffffff; }"
	if _widget != None:
		if type(_widget) in QPushButton:
			return "QPushButton { background-color:" + background_color + "; border-style: " + border[1] + "; border-width: " + border[0] + "; border-color: #454545; color: #ffffff; } QPushButton:hover { background-color:#000000; border-style: solid; border-width: 3px; border-color: #ffd37f; color: #ffffff; }"
'''

def MainL():
	global window, RootMod, EditRoot, DefaultFileSave

	

	

	StyleSheetList0 = ["QPushButton { background-image : url(gui.png); border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover { background-color:#000000; border-style: solid; border-width: 3px; border-color: #ffd37f; color: #ffffff; }", "QPushButton { background-color:#00000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover { background-color:#00000000; border-style: solid; border-width: 3px; border-color: #ffd37f; color: #ffffff; }"]
	StyleSheetList = ["QPushButton { background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover { background-color:#000000; border-style: solid; border-width: 3px; border-color: #ffd37f; color: #ffffff; }", "QPushButton { background-color:#00000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QPushButton:hover { background-color:#00000000; border-style: solid; border-width: 3px; border-color: #ffd37f; color: #ffffff; }", "QPushButton { background-color:#000000; border-style: solid; border-width: 1px; border-color: #454545; color: #ffffff; } QPushButton:hover { background-color:#000000; border-style: solid; border-width: 1px; border-color: #ffd37f; color: #ffffff; } QPushButton:disabled { background-color:#000000; border-style: solid; border-width: 1px; border-color: #84f490; color: #ffffff; }"]
	


	def CloseMod():
		global TempZipPath, RootMod, ContentObject
		TempZipPath = ""
		RootMod = [{}, ""]
		ContentObject = {"Mod": {}, "Path": None, "Type": ["", ""], "Text": ""}


		getOpenMode.hide()

		ModCloseButton.hide()
		ModSaveButton.hide()
		ModChoseButton.show()
		ModNewButton.show()


		Logo = Image.open("resources/icons/noneMod.png")


		ModContentFrame.setAllText("", "", "")

		IconMod.setPixmap(pillowToPixmap(Logo))

		tree.hide()
		
		CloseContentObject()

		SummonMessage("Мод был Закрыт!")

	#_GetOpenMode = QWidget()
	#_GetOpenMode.setStyleSheet("background-color: #252525")
	#_GetOpenMode.setWindowTitle("Открыть Мод Как?")


	class GetOpenMode(DrawWindow):
		def __init__(self):
			super().__init__()
			self.upPanel.setTitle("Открыть Мод Как?")
			self.setMinimumSize(300, 75)
			self.setMaximumSize(300, 75)
			self.resize(300, 75)
			self.upPanel.closeWindow()

			self.layout = QGridLayout(self)

			self._Label = QLabel("Каким способом открыть мод?")
			self._Label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
			self._Label.setFont(QFont(families[0], 12))
			self._Label.setStyleSheet("color: #ffffff")


			self.button0 = QPushButton("Папка")
			self.button0.setStyleSheet(StyleSheetList[0])
			self.button0.setFont(QFont(families[0], 12))
			self.button0.clicked.connect(lambda: OpenMod(0))

			self.button1 = QPushButton("Архив")
			self.button1.setStyleSheet(StyleSheetList[0])
			self.button1.setFont(QFont(families[0], 12))
			self.button1.clicked.connect(lambda: OpenMod(1))

			self.layout.addWidget(self._Label, 0, 0, 1, 0)

			self.layout.addWidget(self.button0, 1, 0)
			self.layout.addWidget(self.button1, 1, 1)

	getOpenMode = GetOpenMode()


	
	class GetCreateFile(DrawWindow):
		def __init__(self):
			super().__init__()
			self.upPanel.setTitle("Создать Файл")
			self.upPanel.closeWindow()


			'''_GetCreateFile = QWidget()
			_GetCreateFile.setStyleSheet("background-color: #252525")
			_GetCreateFile.setWindowTitle("Создать Файл")
			_GetCreateFile.resize(300, 300)'''

			self.layout1 = QGridLayout(self)

			self._Label1 = QLabel("Создать Файл Контента")
			self._Label1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
			self._Label1.setFont(QFont(families[0], 12))
			self._Label1.setStyleSheet("color: #ffffff")

			self._tempCheckBoxStyle = "QComboBox { background-color:#000000; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QComboBox:hover { background-color:#454545; border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff; } QComboBox QAbstractItemView { background-color:#000000; border-style: solid; border-width: 3 0 3 0 px; border-color: #454545; color: #ffffff; } QComboBox QAbstractItemView:hover { background-color:#000000; border-style: solid; border-width: 3 0 3 0 px; border-color: #ffd37f; color: #ffffff; }"

			self._formatFileChoose0 = QLabel("Формат Файла: ")
			self._formatFileChoose0.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
			self._formatFileChoose0.setFont(QFont(families[0], 9))
			self._formatFileChoose0.setStyleSheet("color: #ffffff")
			self._formatFileChoose0.setMaximumWidth(100)

			self._formatFileChoose1 = QComboBox(window)
			self._formatFileChoose1.addItem("json")
			self._formatFileChoose1.addItem("hjson")
			self._formatFileChoose1.setStyleSheet(self._tempCheckBoxStyle)
			self._formatFileChoose1.setFont(QFont(families[0], 12))
	
	

			self._rootTypeChoose0 = QLabel("Главний Тип: ")
			self._rootTypeChoose0.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
			self._rootTypeChoose0.setFont(QFont(families[0], 9))
			self._rootTypeChoose0.setStyleSheet("color: #ffffff")
			self._rootTypeChoose0.setMaximumWidth(100)
	

			self._rootTypeChoose1 = QComboBox(window)
			for o in DefaultFileSave.keys():
				if o != "mod":
					self._rootTypeChoose1.addItem(o)
			self._rootTypeChoose1.setStyleSheet(self._tempCheckBoxStyle)
			self._rootTypeChoose1.setFont(QFont(families[0], 12))
	
	
	
	
			self._typeChoose0 = QLabel("Тип Обєкта: ")
			self._typeChoose0.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
			self._typeChoose0.setFont(QFont(families[0], 9))
			self._typeChoose0.setStyleSheet("color: #ffffff")
			self._typeChoose0.setMaximumWidth(100)

			self._typeChoose1 = QComboBox(window)
			#_typeChoose1.addItem("None")
			#_rootTypeChoose1.addItem("items")
			#_rootTypeChoose1.addItem("liquids")
			self._typeChoose1.setStyleSheet(self._tempCheckBoxStyle)
			self._typeChoose1.setFont(QFont(families[0], 12))
	
	
	

			self._nameFile0 = QLabel("Название Файла: ")
			self._nameFile0.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
			self._nameFile0.setFont(QFont(families[0], 9))
			self._nameFile0.setStyleSheet("color: #ffffff")
			self._nameFile0.setMaximumWidth(100)
	

			self._nameFile1 = QLineEdit(window)
			self._nameFile1.setText("content")
			self._nameFile1.setStyleSheet("color: #ffffff; border-style: solid; border-width: 3 px; border-color: #00000000; border-bottom-color: #454545;")
			self._nameFile1.setFont(QFont(families[0], 12))

			def setForType(_text):
				if _text == "None":
					self._nameFile1.setText(self._rootTypeChoose1.currentText())
				else:
					self._nameFile1.setText(_text)

			def setForRootType(_text):
				self._typeChoose1.clear()
				for i in DefaultFileSave[_text].keys():
					if i == _text:
						self._typeChoose1.addItem("None")
					else:
						self._typeChoose1.addItem(i)

			def createContent():
				global RootMod, ContentObject
				_rootType = self._rootTypeChoose1.currentText()
				_type = self._typeChoose1.currentText()
				if self._nameFile1.text() != "content":
					try:
						if _rootType != "mod":
							_filePath = RootMod[1] + "/content/" + _rootType + "/" + self._nameFile1.text() + "." + self._formatFileChoose1.currentText()
							_mod = DefaultFileSave[_rootType][_type]
							_mod["name"] = self._nameFile1.text()
							if self._formatFileChoose1.currentText() == "json":
								_text = json.dumps(DefaultFileSave[_rootType][_type])
							else:
								_text = hjson.dumps(DefaultFileSave[_rootType][_type])

							_file = open(_filePath, "x")
							_file.write(_text)
							_file.close()
							EntryObj(_mod, [_rootType, _type], _filePath, _text)
							#_GetCreateFile.close()
							self.upPanel.closeWindow()
							SummonMessage("Обєкт " + self._nameFile1.text() + "\nСоздан!")
					except Exception as x:
						SummonMessage("[createContent]: " + str(x), "error")
				else:
					SummonMessage("Не все параметри указани!", _window = self)

			self._rootTypeChoose1.currentTextChanged.connect(setForRootType)
			self._typeChoose1.currentTextChanged.connect(setForType)

			self._createButton = QPushButton("Создать")
			self._createButton.setStyleSheet(StyleSheetList[0])
			self._createButton.setFont(QFont(families[0], 12))
			self._createButton.clicked.connect(createContent)

			self.layout1.addWidget(self._Label1, 0, 0, 1, 0)

			self.layout1.addWidget(self._formatFileChoose0, 1, 0)	
			self.layout1.addWidget(self._formatFileChoose1, 1, 1)
	
			self.layout1.addWidget(self._rootTypeChoose0, 2, 0)	
			self.layout1.addWidget(self._rootTypeChoose1, 2, 1)
	
			self.layout1.addWidget(self._typeChoose0, 3, 0)	
			self.layout1.addWidget(self._typeChoose1, 3, 1)
	
			self.layout1.addWidget(self._nameFile0, 4, 0)	
			self.layout1.addWidget(self._nameFile1, 4, 1)

			self.layout1.addWidget(self._createButton, 5, 0, 1, 0)
			#layout1.addWidget(button11, 5, 1)

	
	

	getCreateFile = GetCreateFile()
		
		#_GetCreateFile.show()


	CreateObj = QPushButton(window, text="Создать")
	CreateObj.setFont(QFont(families[0], 12))
	CreateObj.setStyleSheet(StyleSheetList[0])
	CreateObj.clicked.connect(getCreateFile.upPanel.openWindow)


	

	#ModCard = QFrame(window)
	#ModCard.move(0, 0)
	#ModCard.resize(300, 75)
	#ModCard.setStyleSheet("background-color: %s" % "#000000")



	class CardModInfo(QFrame):
		

		def __init__(self):
			super().__init__(window)
			self.move(0, 75)
			self.resize(300, 595)
			self.setStyleSheet("border-style: solid; border-width: 3px; border-color: #454545; background-color: #00000000")

			self.Name = QLabel(window)
			self.Name.setFont(QFont(families[0], 12))
			self.Name.move(77, 10)
			self.Name.resize(225, 20)
			self.Name.setStyleSheet("color: #ffffff")
			
			self.Version = QLabel(window)
			self.Version.setFont(QFont(families[0], 12))
			self.Version.move(77, 28)
			self.Version.resize(225, 20)
			self.Version.setStyleSheet("color: #ffffff")
			
			self.Author = QLabel(window)
			self.Author.setFont(QFont(families[0], 12))
			self.Author.move(77, 45)
			self.Author.resize(225, 20)
			self.Author.setStyleSheet("color: #ffffff")

		def setAllText(self, _name, _version, _author):
			self.Name.setText(_name)
			self.Version.setText(_version)
			self.Author.setText(_author)

	ModContentFrame = CardModInfo()



	class _IconMod(QLabel):
		def __init__(self):
			super().__init__(window)
			self.move(3, 3)
			self.resize(75-6, 75-6)
			self.setFont(QFont(families[0], 8))
			self.setScaledContents(True)
			self.setStyleSheet("border-style: solid; border-width: 3px; border-color: #ffd37f; color: #ffffff")
			self.setAcceptDrops(True)


			

		def dragEnterEvent(self, event):
			self.setText("Заменить\nКартинку?")
			self.setStyleSheet("border-style: dashed; border-width: 3px; border-color: #ffd37f; color: #ffffff")

			if event.mimeData().hasImage:
				event.accept()
			else:
				event.ignore()
		
		def dragLeaveEvent(self, event):
			self.setText("")
			self.setStyleSheet("border-style: solid; border-width: 3px; border-color: #ffd37f; color: #ffffff")
			try:
				self.setPixmap(pillowToPixmap(Image.open(RootMod[1] + "/icon.png")))
			except Exception:
				self.setPixmap(pillowToPixmap(Image.open("resources/icons/noneMod.png")))

		def dropEvent(self, event):
			self.setText("")
			self.setStyleSheet("border-style: solid; border-width: 3px; border-color: #ffd37f; color: #ffffff")
			if event.mimeData().hasImage and RootMod[1] != "":
				#event.setDropAction(QtCore.Qt.CopyAction)
				

				try:
					self.setPixmap(pillowToPixmap(Image.open(event.mimeData().urls()[0].toLocalFile())))

					_imageBuf = Image.open(event.mimeData().urls()[0].toLocalFile()).copy()

					_imageBuf.save(RootMod[1] + "/icon.png")

					_imageBuf.close()


				except Exception as x:
					try:
						self.setPixmap(pillowToPixmap(Image.open(RootMod[1] + "/icon.png")))
					except Exception:
						self.setPixmap(pillowToPixmap(Image.open("resources/icons/noneMod.png")))
					SummonMessage("Произошла Ошыбка при Загрузке Картинки\n" + str(event.mimeData().urls()[0].toLocalFile()) + "\n" + str(x), "error")


				event.accept()
			else:
				event.ignore()

	
	



	ModOpenButton = QPushButton(window)
	ModOpenButton.move(0, 0)
	ModOpenButton.resize(300, 75)
	ModOpenButton.setStyleSheet(StyleSheetList[1])

	IconMod = _IconMod()
	
	ModOpenButton.clicked.connect(lambda: SelLC(Type = "mod"))

	def ModArchiveSave():
		zip_directory(RootMod[1], TempZipPath[:-4])

		SummonMessage("Архив с модом\nСохранен!")

	ModSaveButton = QPushButton(window)
	ModSaveButton.setText("")
	ModSaveButton.setFont(QFont(families[0], 12))
	ModSaveButton.move(300 - (int(75/2) + 15), int(75/2) - 15)
	ModSaveButton.resize(30, 30)
	ModSaveButton.setStyleSheet(StyleSheetList[0])
	ModSaveButton.setToolTip("Сохранить Архив")
	ModSaveButton.clicked.connect(ModArchiveSave)

	ModSaveButton.hide()
	
	ModNewButton = QPushButton(window)
	ModNewButton.setText("")
	ModNewButton.setFont(QFont(families[0], 12))
	ModNewButton.move(300 - (int(75/2) + 15) - 40, int(75/2) - 15)
	ModNewButton.resize(30, 30)
	ModNewButton.setStyleSheet(StyleSheetList[0])
	ModNewButton.setToolTip("Создать Мод")
	#ModNewButton.clicked.connect(ModArchiveSave)

	
	ModCloseButton = QPushButton(window)
	ModCloseButton.setText("")
	ModCloseButton.setFont(QFont(families[0], 12))
	ModCloseButton.move(300 - (int(75/2) + 15) - 40, int(75/2) - 15)
	ModCloseButton.resize(30, 30)
	ModCloseButton.setStyleSheet(StyleSheetList[0])
	ModCloseButton.setToolTip("Закрыть Мод")
	ModCloseButton.clicked.connect(CloseMod)

	ModCloseButton.hide()
	
	ModChoseButton = QPushButton(window)
	ModChoseButton.setText("")
	ModChoseButton.setFont(QFont(families[0], 12))
	ModChoseButton.move(300 - (int(75/2) + 15), int(75/2) - 15)
	ModChoseButton.resize(30, 30)
	ModChoseButton.setStyleSheet(StyleSheetList[0])
	ModChoseButton.setToolTip("Открыть Мод")
	ModChoseButton.clicked.connect(getOpenMode.upPanel.openWindow)
	#ModCloseButton.clicked.connect()



	


	#if len(ModJson["author"]) > 80:
	#	ModAut = Button(window, text = "Автори", font = ("Arial", 8, "normal"), command = AutS)
	#else:
	#	ModAut = Label(window, text = ModJson["author"], font = ("Arial", 10, "normal"), bg = "#ffffff")
	#ModAut.place(anchor = CENTER, relx = 0.675, rely = 0.06)


	#GridTest = QGridLayout(window)
	#GridTest.setGeometry(QtCore.QRect(300, 300, 100, 100))
	#ButtonTest = QPushButton()
	#GridTest.addWidget(ButtonTest, 0, 0)

	#TabLeftW = QTabWidget(window)
	#TabLeftW.setGeometry(0, 75, 300, window.height() - (75 + 30))
	
	
	
	

	class AttachWidgetFrame(QFrame):
		def setBaseGeometry(self, _x, _y, _width, _height):
			self.baseGeometry = QRect(_x, _y, _width, _height)
		def setBaseGeometry(self, qRect):
			self.baseGeometry = qRect
		#def baseGeomety(self):
			#return self.baseGeometry
		def __init__(self):
			super().__init__(window)
			self.setMouseTracking(True)

			self.baseGeometry = self.geometry
			

			
			#self.widgets = _widgets

			'''self.qTimer = QTimer()
			self.qTimer.setInterval(100)
			self.qTimer.timeout.connect(self.update)
			self.qTimer.start()'''

			self.attachedWidget = None

			#self.isAttached = True

			#self.ok = False

			#print(self.titleBarHeight)
		'''def update(self):

			if self.isAttached == False:
				for i in self.widgets:
					self.setStyleSheet("border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff")
				
					if i.attachedWidget != None:
						break
					if i.upPanel.mi:
						self.ok = False
						if QtGui.QCursor.pos().x() - window.x() > self.x() and QtGui.QCursor.pos().x() - window.x() < self.x() + self.width():
							if QtGui.QCursor.pos().y() - window.y() - self.titleBarHeight > self.y() and QtGui.QCursor.pos().y() - window.y() - self.titleBarHeight < self.y() + self.height():
								#print(self.mousePos.x())
								self.setStyleSheet("border-style: dashed; border-width: 3px; border-color: #ffd37f; color: #ffffff")
								self.ok = True

								

					else:
						if self.ok:
							if QtGui.QCursor.pos().x() - window.x() > self.x() and QtGui.QCursor.pos().x() - window.x() < self.x() + self.width():
								if QtGui.QCursor.pos().y() - window.y() - self.titleBarHeight > self.y() and QtGui.QCursor.pos().y() - window.y() - self.titleBarHeight < self.y() + self.height():
									self.setStyleSheet("border-style: solid; border-width: 3px; border-color: #454545; color: #ffffff")
									i.attach(self)
									self.ok = False

									self.isAttached = True

									break'''




	

	
	#GlobalFrameGridFrame = QFrame(window)
	#GlobalFrameGridFrame.move(0, 75)
	#GlobalFrameGridFrame.resize(800, 700-105)

	#GlobalFrameGrid = QHBoxLayout(GlobalFrameGridFrame)
	#GlobalFrameGrid.setSpacing(0)
	
	


	treeWidget = DrawWindow()
	treeWidget.upPanel.setTitle("Древо Контента")
	treeWidget.setMaximumWidth(300)

	layoutTreeWidget = QGridLayout(treeWidget)
	layoutTreeWidget.setSpacing(0)
	#layoutTreeWidget.set


	class CustomizationWindow():
		def timer(self):

			if self.editorWidgetFrame.attachedWidget != None:
				editorGeometry = QRect(self.editorWidgetFrame.attachedWidget.geometry())
			else:
				editorGeometry = QRect(0, 0, int(window.width()/2), 0)
					
			if self.treeWidgetFrame.attachedWidget != None:
				treeGeometry = QRect(self.treeWidgetFrame.attachedWidget.geometry())
			else:
				treeGeometry = QRect(0, 0, int(window.width()/2), 0)



			if self.editorWidgetFrame.attachedWidget != None:
				#self.treeWidgetFrame.attachedWidget.resize(self.treeWidgetFrame.attachedWidget.width(), 800-105)

				#if self.treeWidgetFrame.attachedWidget != None:
				self.editorWidgetFrame.move(window.width() - editorGeometry.width(), 75)
				self.editorWidgetFrame.resize(window.width() - treeGeometry.width(), window.height()-105)


			else:
				#if self.treeWidgetFrame.attachedWidget != None:
				self.editorWidgetFrame.move(self.treeWidgetFrame.width(), 75)
				self.editorWidgetFrame.resize(window.width() - treeGeometry.width(), window.height()-105)
				#else:
				#	self.editorWidgetFrame.move(int(window.width()/2), 75)
				#	self.editorWidgetFrame.resize(int(window.width()/2), window.height()-105)
			if self.treeWidgetFrame.attachedWidget == None:
				


				#if self.editorWidgetFrame.attachedWidget != None:
				self.treeWidgetFrame.resize(window.width() - editorGeometry.width(), window.height()-105)
				#else:
				#	self.treeWidgetFrame.resize(int(window.width()/2), window.height()-105)
			else:
				self.treeWidgetFrame.attachedWidget.resize(treeGeometry.width(), window.height()-105)
				self.treeWidgetFrame.resize(treeGeometry.width(), window.height()-105)
		def __init__(self):
			self.treeWidgetFrame = AttachWidgetFrame()
			self.editorWidgetFrame = AttachWidgetFrame()

			self.treeWidgetFrame.move(0, 75)
			self.treeWidgetFrame.resize(int(window.width()/2), window.height()-105)

			self.editorWidgetFrame.move(int(window.width()/2), 75)
			self.editorWidgetFrame.resize(int(window.width()/2), window.height()-105)
			#self.editorWidgetFrame.move(300, 75)
			#self.editorWidgetFrame.resize(700, 800-105-300)
			#self.editorWidgetFrame.

			self.qTimer = QTimer()
			self.qTimer.setInterval(100)
			self.qTimer.timeout.connect(self.timer)
			self.qTimer.start()
	
	customizationWindow = CustomizationWindow()
	

	#GlobalFrameGrid.addWidget(customizationWindow.treeWidgetFrame, 4)
	#GlobalFrameGrid.addWidget(customizationWindow.editorWidgetFrame, 6)

	treeWidget.upPanel.openWindow()

	attachebleWidgets.append(customizationWindow.treeWidgetFrame)
	attachebleWidgets.append(customizationWindow.editorWidgetFrame)
	#attachebleWidgets.append(getOpenMode)
	#attachebleWidgets.append(getCreateFile)

	treeWidgetOpener = QPushButton(window)
	treeWidgetOpener.move(300-30, 700-30)
	treeWidgetOpener.resize(30, 30)
	treeWidgetOpener.setText("")
	treeWidgetOpener.setFont(QFont(families[0], 10))
	treeWidgetOpener.setStyleSheet(StyleSheetList[0])
	treeWidgetOpener.clicked.connect(lambda: treeWidget.attach(customizationWindow.treeWidgetFrame))
	
	editorWidgetOpener = QPushButton(window)
	editorWidgetOpener.move(300-30-30, 700-30)
	editorWidgetOpener.resize(30, 30)
	editorWidgetOpener.setText("")
	editorWidgetOpener.setFont(QFont(families[0], 10))
	editorWidgetOpener.setStyleSheet(StyleSheetList[0])
	editorWidgetOpener.clicked.connect(lambda: editorWindow.attach(customizationWindow.editorWidgetFrame))

	treeWidget.attach(customizationWindow.treeWidgetFrame)
	

	tree = QTreeView(window)
	tree.hide()
	model = QFileSystemModel()
	tree.setStyleSheet("color: #ffffff; border-style: solid; border-width: 3 px; border-color: #454545;")
	#tree.setGeometry(0, 75, 300, window.height() - (75 + 30))

	

	def ChooseTypeContent(_button = None):
		global _tempButtonContent, EditRoot
		if _tempButtonContent == None:
			_type = buttonTreeBlocks.text()
			_button.setDisabled(True)
		else:
			_type = _button.text()
			_button.setDisabled(True)
			_tempButtonContent.setDisabled(False)
		_tempButtonContent = _button

		if os.path.exists(RootMod[1] + "/content/" + _type.lower() + "/"):
			model.setRootPath(RootMod[1] + "/content/" + _type.lower() + "/")

			tree.setModel(model)
			tree.setRootIndex(model.index(RootMod[1] + "/content/" + _type.lower() + "/"))

			tree.setColumnWidth(0, 1000)
			
			tree.show()
		else:
			tree.hide()

		EditRoot[1] = _type



	buttonTreeBlocks = QPushButton(window)
	buttonTreeBlocks.setText("Blocks")
	buttonTreeBlocks.setFont(QFont(families[0], 9))
	buttonTreeBlocks.move(0, 75)
	buttonTreeBlocks.resize(75, 15)
	buttonTreeBlocks.setMaximumSize(75, 15)
	buttonTreeBlocks.setStyleSheet(StyleSheetList[2])
	buttonTreeBlocks.clicked.connect(lambda: ChooseTypeContent(buttonTreeBlocks))
	
	buttonTreeItems = QPushButton(window)
	buttonTreeItems.setText("Items")
	buttonTreeItems.setFont(QFont(families[0], 9))
	buttonTreeItems.move(0, 90)
	buttonTreeItems.resize(75, 15)
	buttonTreeItems.setMaximumSize(75, 15)
	buttonTreeItems.setStyleSheet(StyleSheetList[2])
	buttonTreeItems.clicked.connect(lambda: ChooseTypeContent(buttonTreeItems))
	
	buttonTreeLiquids = QPushButton(window)
	buttonTreeLiquids.setText("Liquids")
	buttonTreeLiquids.setFont(QFont(families[0], 9))
	buttonTreeLiquids.move(75, 75)
	buttonTreeLiquids.resize(75, 15)
	buttonTreeLiquids.setMaximumSize(75, 15)
	buttonTreeLiquids.setStyleSheet(StyleSheetList[2])
	buttonTreeLiquids.clicked.connect(lambda: ChooseTypeContent(buttonTreeLiquids))
	
	buttonTreeSectors = QPushButton(window)
	buttonTreeSectors.setText("Sectors")
	buttonTreeSectors.setFont(QFont(families[0], 9))
	buttonTreeSectors.move(75, 90)
	buttonTreeSectors.resize(75, 15)
	buttonTreeSectors.setMaximumSize(75, 15)
	buttonTreeSectors.setStyleSheet(StyleSheetList[2])
	buttonTreeSectors.clicked.connect(lambda: ChooseTypeContent(buttonTreeSectors))
	
	buttonTreeStatus = QPushButton(window)
	buttonTreeStatus.setText("Status")
	buttonTreeStatus.setFont(QFont(families[0], 9))
	buttonTreeStatus.move(150, 75)
	buttonTreeStatus.resize(75, 15)
	buttonTreeStatus.setMaximumSize(75, 15)
	buttonTreeStatus.setStyleSheet(StyleSheetList[2])
	buttonTreeStatus.clicked.connect(lambda: ChooseTypeContent(buttonTreeStatus))
	
	buttonTreeUnits = QPushButton(window)
	buttonTreeUnits.setText("Units")
	buttonTreeUnits.setFont(QFont(families[0], 9))
	buttonTreeUnits.move(150, 90)
	buttonTreeUnits.resize(75, 15)
	buttonTreeUnits.setMaximumSize(75, 15)
	buttonTreeUnits.setStyleSheet(StyleSheetList[2])
	buttonTreeUnits.clicked.connect(lambda: ChooseTypeContent(buttonTreeUnits))
	
	buttonTreeWeathers = QPushButton(window)
	buttonTreeWeathers.setText("Weathers")
	buttonTreeWeathers.setFont(QFont(families[0], 9))
	buttonTreeWeathers.move(225, 75)
	buttonTreeWeathers.resize(75, 30)
	buttonTreeWeathers.setMaximumSize(75, 30)
	buttonTreeWeathers.setMinimumSize(75, 30)
	buttonTreeWeathers.setStyleSheet(StyleSheetList[2])
	buttonTreeWeathers.clicked.connect(lambda: ChooseTypeContent(buttonTreeWeathers))

	
	layoutTreeWidget.addWidget(buttonTreeBlocks, 0, 0)
	layoutTreeWidget.addWidget(buttonTreeItems, 1, 0)
	layoutTreeWidget.addWidget(buttonTreeLiquids, 0, 1)
	layoutTreeWidget.addWidget(buttonTreeSectors, 1, 1)
	layoutTreeWidget.addWidget(buttonTreeStatus, 0, 2)
	layoutTreeWidget.addWidget(buttonTreeUnits, 1, 2)
	layoutTreeWidget.addWidget(buttonTreeWeathers, 0, 3, 2, 1)

	layoutTreeWidget.addWidget(tree, 2, 0, 3, 0)




	def ImagOPT(img):
		for t in range(0, len(SpriteL)):
			if SpriteL[t][-1*(len(img)):] == img:
				return SpriteL[t]
				break
		return "error.png"

	

	class EditorWindow(DrawWindow):
		def __init__(self):
			super().__init__()
			self.upPanel.setTitle("Редактор")
			pass

	editorWindow = EditorWindow()
	editorWindow.attach(customizationWindow.editorWidgetFrame)


	EObj = {"img": QLabel(window),
	 "type": [QLabel(editorWindow, text = "Type"), QComboBox(editorWindow)],
	 "name": [QLabel(editorWindow, text = "Name"), QLineEdit(editorWindow)],
	 "displayName": [QLabel(editorWindow, text = "DisplayName"), QLineEdit(editorWindow)], 
	 "author": [QLabel(editorWindow, text = "Authors"), QLineEdit(editorWindow)], 
	 "description": [QLabel(editorWindow, text = "Description"), QTextEdit(editorWindow)], 
	 "version": [QLabel(editorWindow, text = "Version"), QLineEdit(editorWindow)], 
	 "minGameVersion": [QLabel(editorWindow, text = "minVersion"), QLineEdit(editorWindow)], 
	 "dependencies": [QLabel(editorWindow, text = "dependencies"), QLineEdit(editorWindow), list], 
	 "hidden": [QLabel(editorWindow, text = "hidden"), QCheckBox(editorWindow)], 

	 "health": [QLabel(editorWindow, text = "Health"), QLineEdit(editorWindow), float], 
	 "size": [QLabel(editorWindow, text = "Size"), QLineEdit(editorWindow), float], 
	 "speed": [QLabel(editorWindow, text = "Speed"), QLineEdit(editorWindow), float], 

	 "hasPower": [QLabel(editorWindow, text = "hasPower"), QCheckBox(editorWindow)], 
	 "hasItems": [QLabel(editorWindow, text = "hasItems"), QCheckBox(editorWindow)], 
	 "hasLiquids": [QLabel(editorWindow, text = "hasLiquids"), QCheckBox(editorWindow)], 

	 "craftTime": [QLabel(editorWindow, text = "craftTime"), QLineEdit(editorWindow), float], 
	 "idleSoundVolume": [QLabel(editorWindow, text = "idleSoundVolume"), QLineEdit(editorWindow), float], 
	 "itemCapacity": [QLabel(editorWindow, text = "itemCapacity"), QLineEdit(editorWindow), float], 

	 "updateEffect": [QLabel(editorWindow, text = "updateEffect"), QLineEdit(editorWindow)], 

	 "drillTime": [QLabel(editorWindow, text = "Drill Time"), QLineEdit(editorWindow), float], 
	 "drillEffect": [QLabel(editorWindow, text = "Drill Effect"), QLineEdit(editorWindow)], 

	 "tier": [QLabel(editorWindow, text = "Tier"), QLineEdit(editorWindow), float], 

	 "heating": [QLabel(editorWindow, text = "Heating"), QLineEdit(editorWindow), float], 

	 "powerProduction": [QLabel(editorWindow, text = "Power Production"), QLineEdit(editorWindow), float], 
	 "itemDuration": [QLabel(editorWindow, text = "Item Duration"), QLineEdit(editorWindow), float], 



	 "requirements": [QLabel(editorWindow, text = "Requirements"), QLineEdit(editorWindow)], 
	 "consumes": [QLabel(editorWindow, text = "Consumes"), QLineEdit(editorWindow)], 
	 "outputItem": [QLabel(editorWindow, text = "Output Item"), QLineEdit(editorWindow)], 
	 "outputLiquid": [QLabel(editorWindow, text = "Output Liquid"), QLineEdit(editorWindow)], 

	 "category": [QLabel(editorWindow, text = "Category"), QLineEdit(editorWindow)], 
	 "research": [QLabel(editorWindow, text = "Research"), QLineEdit(editorWindow)], 
	 "alwaysUnlocked": [QLabel(editorWindow, text = "Always Unlocked"), QCheckBox(editorWindow)], 

	 "color": [QLabel(editorWindow, text = "Color"), QLineEdit(editorWindow)], 
	 "explosiveness": [QLabel(editorWindow, text = "Explosiveness"), QLineEdit(editorWindow), float], 
	 "fliammbility": [QLabel(editorWindow, text = "Fliammbility"), QLineEdit(editorWindow), float], 
	 "radioactivity": [QLabel(editorWindow, text = "Radioactivity"), QLineEdit(editorWindow), float], 
	 "hardness": [QLabel(editorWindow, text = "Hardness"), QLineEdit(editorWindow), float], 
	 "cost": [QLabel(editorWindow, text = "Cost"), QLineEdit(editorWindow), float], 

	 "healthScaling": [QLabel(editorWindow, text = "Health Scaling"), QLineEdit(editorWindow), float], 
	 "lowPriority": [QLabel(editorWindow, text = "Low Priority"), QLineEdit(editorWindow), float], 
	 "frames": [QLabel(editorWindow, text = "Frames"), QLineEdit(editorWindow), float], 
	 "transitionFrames": [QLabel(window, text = "Transition Frames"), QLineEdit(editorWindow), float], 
	 "frameTime": [QLabel(editorWindow, text = "Frame Time"), QLineEdit(editorWindow), float], 
	 "buildable": [QLabel(editorWindow, text = "Buildable"), QLineEdit(editorWindow), float], 





	 "viscosity": [QLabel(editorWindow, text = "Viscosity"), QLineEdit(editorWindow), float], 
	 "heatCapacity": [QLabel(editorWindow, text = "Heat Capacity"), QLineEdit(editorWindow), float], 
	 "effect": [QLabel(editorWindow, text = "Effect"), QLineEdit(editorWindow)], 
	 "lightColor": [QLabel(editorWindow, text = "Light Color"), QLineEdit(editorWindow)], 
	}

	def GetContentObjectData():
		global ContentObject, DefaultFileSave
		ModSaveTemp = None
		try:
			if ContentObject["Type"][0] != None:
				print(ContentObject["Type"])
				if ContentObject["Mod"] != {}:
					if ContentObject["Type"][1] in DefaultFileSave[ContentObject["Type"][0]]:
						ModSaveTemp = DefaultFileSave[ContentObject["Type"][0]][ContentObject["Type"][1]]
					elif ContentObject["Type"][0] == "mod":
						ModSaveTemp = DefaultFileSave["mod"]
					elif ContentObject["Type"][0] in DefaultFileSave[ContentObject["Type"][0]]:
						ModSaveTemp = DefaultFileSave[ContentObject["Type"][0]][ContentObject["Type"][0]]
					
					print("= ", ModSaveTemp, " =")
					ModSaveTemp_temp = ModSaveTemp
					for i in ModSaveTemp.keys():
						try:
							if type(EObj[i][1]) is QTextEdit:
								if len(EObj[i][1].toPlainText()) > 0:
									ModSaveTemp[i] = EObj[i][1].toPlainText()
								else:
									ModSaveTemp[i] = None
							if type(EObj[i][1]) is QLineEdit:
								if len(EObj[i][1].text()) > 0:
									ModSaveTemp[i] = EObj[i][1].text()
								else:
									ModSaveTemp[i] = None
							if type(EObj[i][1]) is QComboBox:
								if len(EObj[i][1].currentText()) > 0:
									ModSaveTemp[i] = EObj[i][1].currentText()
								else:
									ModSaveTemp[i] = None
							if type(EObj[i][1]) is QCheckBox:
								ModSaveTemp[i] = EObj[i][1].isChecked()
							if list is type(ModSaveTemp_temp[i]):
									
								_tempCon = ""

								for o in ModSaveTemp[i]:
									if o == "'":
										_tempCon += '"'
									else:
										_tempCon += o
								ModSaveTemp[i] = _tempCon

								ModSaveTemp[i] = json.loads(str(ModSaveTemp[i]))

							if float is type(ModSaveTemp_temp[i]):
								ModSaveTemp[i] = float(ModSaveTemp[i])
							if int is type(ModSaveTemp_temp[i]):
								ModSaveTemp[i] = int(ModSaveTemp[i])

								
						except Exception as x:
							print(type(EObj[i][1]))
							print(x)
							SummonMessage(x, "error")

						print("HI")
							
					return ModSaveTemp
		except Exception as x:
			SummonMessage(x, "error")

	def ModSave():
		global ContentObject, EditRoot
		print(ContentObject["Mod"])
		try:
			if EditRoot[0] == 0:
				if ContentObject["Mod"] != {}:
					ModSaveTemp = GetContentObjectData()
					print(ModSaveTemp)
					if ModSaveTemp != None:
						_tttemp = ContentObject["Path"]
						if getSuffixPath(_tttemp) == "json":
							with open(_tttemp, "w") as _tempSave:
								json.dump(ModSaveTemp, _tempSave)
						if getSuffixPath(_tttemp) == "hjson":
							os.rename(_tttemp, _tttemp[:-5] + "json")
							_tttemp = _tttemp[:-5] + "json"
							ContentObject["Path"] = _tttemp
							if ContentObject["Type"][0] == "mod":
								ContentObject["Type"][1] = "json"

							SummonMessage("Для Лутшой Работи Програми\nВсе данние переконвертировани под Json")
							with open(_tttemp, "w") as _tempSave:
								json.dump(ModSaveTemp, _tempSave)
				_read = openFiler(ContentObject["Path"])
				print("HEAR")
				print(_read)
				ContentObject["Mod"] = _read[0]
				ContentObject["Text"] = _read[1]
				OpenPreContentObject()
			elif EditRoot[0] == 1:
				ModSaveTemp = ModeEditText.toPlainText()
				print(ModSaveTemp)
				_tttemp = ContentObject["Path"]
				if getSuffixPath(_tttemp) == "json":
					with open(_tttemp, "w") as _tempSave:
						json.dump(ModSaveTemp, _tempSave)
				if getSuffixPath(_tttemp) == "hjson":
					with open(_tttemp, "w") as _tempSave:
						hjson.dump(ModSaveTemp, _tempSave)
				_read = openFiler(ContentObject["Path"])
				ContentObject["Mod"] = _read[0]
				ContentObject["Text"] = _read[1]
				OpenPreContentObject()
			SummonMessage("Контент Сохранен!")
		except Exception as x:
			SummonMessage(x, "error")
	EobjTemp = [0, 0, 0]
	def EObjOP(par, _text = None, _add = 0, _addSizeY = 15):


		try:
			EObj[par][0].hide()
			EObj[par][1].hide()
		except Exception:
			EObj[par].hide()

		Text = _text

		
		if type(_text) is list:
			if len(_text) == 1:
				if type(_text[0]) is dict:
					if par in _text[0]:
						Text = _text[0][par]
					else:
						Text = None


		

		if Text != None:
			if _add >= 1 and EobjTemp[1] == 0:
				EobjTemp[1] = _add
				EobjTemp[2] = _add
			if type(Text) is str or type(Text) is bool or type(Text) is list or  type(Text) is int or type(Text) is float or type(Text) is dict or type(Text) is collections.OrderedDict:
				EObj[par][0].show()
				EObj[par][1].show()

				'''if _add == 1 and EobjTemp[1] == 0:
					EObj[par][0].setGeometry(305, 80 + EobjTemp[0], 100, _addSizeY)
					EObj[par][1].setGeometry(305 + 105, 80 + EobjTemp[0], int((window.width()-300)/2)-125, _addSizeY)
				elif _add == 0 and EobjTemp[1] == 1:
					EObj[par][0].setGeometry(305 + int((window.width()-300)/2), 80 + EobjTemp[0], 100, _addSizeY)
					EObj[par][1].setGeometry(305 + 105 + int((window.width()-300)/2), 80 + EobjTemp[0], int((window.width()-300)/2)-125, _addSizeY)
				else:
					EObj[par][0].setGeometry(305, 80 + EobjTemp[0], 100, _addSizeY)
					EObj[par][1].setGeometry(305 + 105 + int((window.width()-300)/_add), 80 + EobjTemp[0], int((window.width()-300)/_add)-125, _addSizeY)'''
			
				
				_windowWidth = editorWindow.width()
				#_windowWidth = window.width()-300

				if EobjTemp[1] != 0:
					if EobjTemp[1] != 1:
						_delWindow = int(((_windowWidth)/EobjTemp[2])*(EobjTemp[1] - 1))
					else:
						_delWindow = 0

					EObj[par][0].setGeometry(7 + _delWindow, 7 + EobjTemp[0], 100, _addSizeY)
					EObj[par][1].setGeometry(7 + 105 + _delWindow, 7 + EobjTemp[0], int((_windowWidth)/EobjTemp[2])-125, _addSizeY)
				else:
					EObj[par][0].setGeometry(7, 7 + EobjTemp[0], 100, _addSizeY)
					EObj[par][1].setGeometry(7 + 105, 7 + EobjTemp[0], (_windowWidth)-125, _addSizeY)
				EObj[par][0].setFont(QFont(families[0], 7))
				EObj[par][1].setFont(QFont(families[0], 7))

				EObj[par][0].setStyleSheet("color: #ffffff")
				EObj[par][1].setStyleSheet("color: #ffffff")
				
				if type(EObj[par][1]) is QComboBox:
					EObj[par][1].clear()
					EObj[par][1].addItem(str(Text))
					EObj[par][1].setCurrentIndex(0)
				elif type(EObj[par][1]) is QCheckBox:
					EObj[par][1].setChecked(bool(Text))
				else:
					if type(_text) is collections.OrderedDict:
						EObj[par][1].setText(str(json.loads(json.dumps(Text))))
					else:
						EObj[par][1].setText(str(Text))
					EObj[par][1].setStyleSheet("color: #ffffff; border-style: solid; border-width: 3 px; border-color: #00000000; border-bottom-color: #454545; padding: -15 px;")

				if _add == 0 and EobjTemp[1] <= 1:
					EobjTemp[0] += _addSizeY + 5
					EobjTemp[1] = 0
					EobjTemp[2] = 0

				else:
					EobjTemp[1] -= 1
				

	ModeEditButton = QPushButton(window, text="Режим Редактирования\nГрафический")
	ModeEditButton.setFont(QFont(families[0], 10))
	ModeEditButton.setStyleSheet(StyleSheetList[0])
	ModeEditButton.hide()
	
	ModeEditText = QTextEdit(window)
	ModeEditText.setFont(QFont(families[0], 10))
	ModeEditText.move(305, 75)
	ModeEditText.resize(490, 590)
	ModeEditText.setStyleSheet("color: #ffffff")
	ModeEditText.hide()


	
			
	Desc_Content = QLabel(window)
	Desc_Content.setFont(QFont(families[0], 12))
	Desc_Content.move(377, 30)
	Desc_Content.resize(225, 40)
	Desc_Content.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
	Desc_Content.setStyleSheet("color: #ffffff")
	
	Name_Content = QLabel(window)
	Name_Content.setFont(QFont(families[0], 12))
	Name_Content.move(377, 10)
	Name_Content.resize(225, 15)
	Name_Content.setStyleSheet("color: #ffd37f")

	Frame_Content = QPushButton(window)
	Frame_Content.move(300, 0)
	Frame_Content.resize(300, 75)
	Frame_Content.setStyleSheet("border-style: solid; border-width: 3px; border-color: #454545; background-color: #00000000")

	SaveObj = QPushButton(window)
	SaveObj.setText("")
	SaveObj.setFont(QFont(families[0], 12))
	SaveObj.move(300 - (int(75/2) + 15), int(75/2) - 15)
	SaveObj.resize(30, 30)
	SaveObj.setStyleSheet(StyleSheetList[0])
	SaveObj.setToolTip("Сохранить Контент")
	SaveObj.clicked.connect(lambda: ModSave())

	SaveObj.hide()
	
	CloseObj = QPushButton(window)
	CloseObj.setText("")
	CloseObj.setFont(QFont(families[0], 12))
	CloseObj.move(300 - (int(75/4) + 15), int(75/2) - 15)
	CloseObj.resize(30, 30)
	CloseObj.setStyleSheet(StyleSheetList[0])
	CloseObj.setToolTip("Закрить Контент")
	CloseObj.clicked.connect(lambda: CloseContentObject())

	CloseObj.hide()
	
	

	


	def CloseContentObject():
		global ContentObject, TempMod
		ContentObject = {"Mod": {}, "Path": None, "Type": ["", ""], "Text": ""}

		for op in EObj:
			EObjOP(op)
		
		ModeEditText.hide()

		Name_Content.hide()
		Desc_Content.hide()

		SaveObj.hide()
		CloseObj.hide()

		ModeEditButton.hide()

		TempMod = None





	def OpenMod(_mode = 0):
		global RootMod, TempZipPath

		TempZipPath = ""


		getOpenMode.upPanel.closeWindow()

		ModCloseButton.hide()
		ModSaveButton.hide()
		ModChoseButton.show()
		ModNewButton.show()
			
		try:

			sucsFold = False
			while sucsFold == False:
				if _mode == 0:
					Mod1 = QFileDialog.getExistingDirectory(window, "Выберете папку с модом", os.path.expanduser('~') + "\\AppData\\Roaming\\Mindustry\\mods\\")

				else:
					try:
						shutil.rmtree("ZipTemp")
					except Exception:
						pass
					os.mkdir("ZipTemp")
					Mod1 = QFileDialog.getOpenFileName(window, "Выберете Архив с модом", os.path.expanduser('~') + "\\AppData\\Roaming\\Mindustry\\mods\\", "*.zip")
	
					TempZipPath = Mod1[0]
				
					
					ModSaveButton.show()
					ModChoseButton.hide()
					
				
					shutil.unpack_archive(Mod1[0], "ZipTemp", "zip")

					Mod1 = "ZipTemp"
					print(Mod1)
				ModNewButton.hide()
				ModCloseButton.show()

				Mod = os.listdir(Mod1)
				print(Mod)
				for i in Mod:
					if i == "mod.json" or i == "mod.hjson":
						sucsFold = True
						RootMod[0] = openFiler(Mod1 + "/" + i)[0]
						break
				if sucsFold == False and len(Mod) == 1:
					Mod1 = Mod1 + "/" + Mod[0]
					Mod = os.listdir(Mod1)
					for i in Mod:
						if i == "mod.json" or i == "mod.hjson":
							sucsFold = True
							RootMod[0] = openFiler(Mod1 + "/" + i)[0]
							break
				print(RootMod[0])
				RootMod[1] = Mod1
				if sucsFold == False:
					msgBox = QMessageBox(window)
					msgBox.setFont(QFont(families[0], 12))
					msgBox.setStyleSheet(StyleSheetList[0] + "QMessageBox QLabel {color: #ffffff;}")
					msgBox.setText("Мод не обнаружен!\nПопробуйте еще раз!")
					msgBox.exec()
			#RootMod[1] = Mod1

			InitializationMod()
		except Exception as x:
			SummonMessage(x, "error")
			CloseMod()
	
	

	def InitializationMod():
		global RootMod, ContentL, ContentL1, SpriteL, ContentObject
		
		print(RootMod[1])
		print(RootMod[0])
		
		try:
			if RootMod[0] == None:
				msgBox = QMessageBox(window)
				#msgBox.setIcon(QMessageBox.warning)
				msgBox.setText("Файл с информациєй о моде не возможно открить или же он бил поврежден!\nВозможни проблеми: Кодировка файла или же руские символи!\nФайл бил востоновлен!")
				SummonMessage("Файл Востоновлен!")
				msgBox.setFont(QFont(families[0], 12))
				msgBox.setStyleSheet(StyleSheetList[0] + "QMessageBox QLabel {color: #ffffff;}")
				msgBox.exec()

			

				RootMod[0] = DefaultFileSave["mod"]

				if os.path.exists(RootMod[1] + "/mod.hjson"):
					SummonMessage("Файл <mod.hjson> бил востоновлен!")
				if os.path.exists(RootMod[1] + "/mod.json"):
					SummonMessage("Файл <mod.json> бил востоновлен!")

				ModSave()

			ContentL = []
			ContentL1 = []
			SpriteL = []

			for root, dirs, files in os.walk(RootMod[1] + "/content"):
				for file in files:
					if file.endswith(".json") or file.endswith(".hjson"):
						ContentL.append(str(os.path.join(root, file)))
						ContentL1.append(file)

			for root, dirs, files in os.walk(RootMod[1] + "/sprites"):
				for file in files:
					if file.endswith(".png"):
						SpriteL.append(str(os.path.join(root, file)))

			


			try:
				if os.path.exists(RootMod[1] + "/icon.png"):
					Logo = Image.open(RootMod[1] + "/icon.png")
				else:
					Logo = Image.open("resources/icons/noneMod.png")
			except Exception:
				Logo = Image.open("resources/icons/noneMod.png")

			_ttt = ["name", "version", "author"]
			for p in range(len(_ttt)):
				try:
					if "displayName" in RootMod[0] and _ttt[p] == "name":
						_ttt[p] = coloritaText(str(RootMod[0]["displayName"]))
					else:
						_ttt[p] = coloritaText(str(RootMod[0][_ttt[p]]))
				except:
					_ttt[p] = coloritaText("[red]None")

			ModContentFrame.setAllText(_ttt[0], _ttt[1], _ttt[2])




			IconMod.setPixmap(pillowToPixmap(Logo))

			tree.hide()
		
			CloseContentObject()

			SummonMessage("Мод был Открыт!")
		except Exception:
			SummonMessage("Мод был Открыт С Ошыбками!")

		
	'''Функция Перезаписи Размера'''

	'''Функция Перезаписи Размера'''

	'''Функция Перезаписи Размера'''

	'''Функция Перезаписи Размера'''

	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''
	'''Функция Перезаписи Размера'''

	devVersionLabel = QLabel(window)
	devVersionLabel.setText("Final-Alpha")
	devVersionLabel.setStyleSheet("background: #252525; color: #ffd37f; border: 3 solid #ffd37f")
	devVersionLabel.setFont(QFont(families[0], 12))
	devVersionLabel.setAlignment(QtGui.Qt.AlignmentFlag.AlignRight)



	def ResizeWindow():
		try:
			#tree.setGeometry(0, 75, 300, window.height() - (75 + 30))
			CreateObj.setGeometry(0, int(window.height() - 30), 75, 30)
			ModeEditButton.setGeometry(int((window.width() - 300)/2 + 300 -100), int(window.height() - 30), 200, 30)

			ModContentFrame.setGeometry(0, 75, 300, window.height() - (75 + 30))

			#GlobalFrameGridFrame.setGeometry(0, 75, window.width(), window.height() - (75 + 30))
			Frame_Content.resize(window.width() - 300, 75)

			treeWidgetOpener.move(300-30, window.height()-30)
			editorWidgetOpener.move(300-60, window.height()-30)

			Name_Content.resize(window.width() - 377, 20)
			Desc_Content.resize(window.width() - 377, 40)
			SaveObj.move(window.width() - (int(75/2) + 15) - 40, int(75/2) - 15)
			CloseObj.move(window.width() - (int(75/2) + 15), int(75/2) - 15)

			devVersionLabel.setGeometry(int(window.width() - 150), int(window.height() - 30), 150, 30)
			devVersionLabel.raise_()
		except Exception as x:
			SummonMessage(x, "error")

	def MessageDeleteInfo(i):
		print(i)
		buferMessage[i]["them_info"] = 2

	def MessageUpdate():
		n = 0
		#try:
		if 1==1:
			for i in buferMessage:
				
				if i["them"] == "info":
					if "them_info" in i:
						if i["them_info"] == 0:
							if i["widget"].y() < 0:
								i["widget"].move(int(i["window"].width()/2 - i["widget"].width()/2), i["widget"].y() + 1)
								if i["widget"].y() >= 0:
									i["them_info"] = 1
									QTimer.singleShot(5000, lambda: MessageDeleteInfo(n-1))
						elif i["them_info"] == 2:
							i["widget"].move(int(i["window"].width()/2 - i["widget"].width()/2), i["widget"].y() - 1)
							if i["widget"].y() < (i["widget"].height() * -1):
								i["widget"].deleteLater()
								buferMessage.remove(i)
								break
					else:
						i.update({"them_info": 0})
				else:
					if i["widget"].y() > int(i["window"].height()/4) + (i["widget"].height() + 15 * 2):
						i["widget"].deleteLater()
						buferMessage.remove(i)
						break
					i["widget"].move(int(i["window"].width()/2 - i["widget"].width()/2), i["widget"].y() + 1)
					#print(max(min(int(i.height()/39), 1), 0.1))
				n += 1
		#except Exception as x:
			#print(x)


	window.qTimer = QTimer()
	window.qTimer.setInterval(100)
	window.qTimer.timeout.connect(ResizeWindow)
	window.qTimer.start()

	window.q1Timer = QTimer()
	window.q1Timer.setInterval(10)
	window.q1Timer.timeout.connect(MessageUpdate)
	window.q1Timer.start()


	ResizeWindow()
	#window.resized.connect(ResizeWindow)


	




	def EditModChose():
		global EditRoot, ContentObject
		_temp = ContentObject
		CloseContentObject()
		ContentObject = _temp

		try:

			ContentObject["Mod"] = openFiler(ContentObject["Path"])
			OpenPreContentObject()

			if EditRoot[0] == 0:
				EditRoot[0] = 1
				ModeEditButton.setText("Режим Редактирования\nТекстовий")

				ModeEditText.show()

				OpenContentObjectText()
			else:
				EditRoot[0] = 0
				ModeEditButton.setText("Режим Редактирования\nГрафический")

				OpenContentObjectGUI()
		except Exception as x:
			SummonMessage(x, "error")


	ModeEditButton.clicked.connect(EditModChose)



	def OpenContentObjectText():
		Text = ContentObject["Text"]
		Type = ContentObject["Type"][1].lower()
		_path = ContentObject["Path"]

		ModeEditButton.show()

		ModeEditText.show()
		ModeEditText.setPlainText(Text)

	def OpenContentObjectGUI():
		ModeEditButton.show()
		Mods = dict(ContentObject["Mod"])
		Type = ContentObject["Type"][1]
		RootType = ContentObject["Type"][0]
		_path = ContentObject["Path"]
		print("=====")
		print(RootType)
		print(Type)
		print("=====")
		#try:
		if 0==0:
			if RootType != None:
				EobjTemp[0] = 0
				EobjTemp[1] = 0
				EobjTemp[2] = 0
				if RootType == "mod":

					RootMod[0] = DefaultFileSave["mod"]
					
					for s in Mods.keys():
						RootMod[0][s] = Mods[s]

					Mods = RootMod[0]

					EObjOP("name", [Mods])
					EObjOP("displayName", [Mods])
					EObjOP("author", [Mods])
					EObjOP("description", [Mods], 0, 120)
					EObjOP("version", [Mods], 2)
					EObjOP("minGameVersion", [Mods])
					EObjOP("dependencies", [Mods], 2)
					EObjOP("hidden", [Mods])

			
				else:
					
					if RootType == "items":
						if Type != "":
							EObjOP("type", Type)
							EObj["type"][1].addItem("None")

							
							ContentObject["Mod"] = DefaultFileSave[RootType][Type]

						else:
							ContentObject["Mod"] = DefaultFileSave[RootType][RootType]

						for s in Mods.keys():
							ContentObject["Mod"][s] = Mods[s]

						Mods = ContentObject["Mod"]
						
						EObjOP("name", [Mods])
						EObjOP("description", [Mods], 0, 120)

						EObjOP("color", [Mods])
						EObjOP("explosiveness", [Mods], 3)
						EObjOP("fliammbility", [Mods])
						EObjOP("radioactivity", [Mods])
						EObjOP("hardness", [Mods], 2)
						EObjOP("cost", [Mods])

						EObjOP("healthScaling", [Mods])
						EObjOP("lowPriority", [Mods])

						EObjOP("frames", [Mods], 3)
						EObjOP("transitionFrames", [Mods])
						EObjOP("frameTime", [Mods])

						EObjOP("buildable", [Mods])

						EObjOP("research", [Mods], 2)
						EObjOP("alwaysUnlocked", [Mods])
					elif RootType == "blocks":
						EObjOP("type", Type)
						EObj["type"][1].addItem("None")
						ContentObject["Mod"] = DefaultFileSave[RootType][Type]
					
						for s in Mods.keys():
							ContentObject["Mod"][s] = Mods[s]

						Mods = ContentObject["Mod"]

						EObjOP("name", [Mods])
						EObjOP("description", [Mods], 0, 120)

						EObjOP("health", [Mods], 2)
						EObjOP("heating", [Mods])
						
						EObjOP("speed", [Mods])
						EObjOP("size", [Mods])
						EObjOP("tier", [Mods])

						EObjOP("hasPower", [Mods], 3)
						EObjOP("hasItems", [Mods])
						EObjOP("hasLiquids", [Mods])

						EObjOP("craftTime", [Mods], 2)
						EObjOP("itemCapacity", [Mods])

						EObjOP("idleSoundVolume", [Mods])
						EObjOP("updateEffect", [Mods])


						if Type == "drill":
							EObjOP("drillTime", [Mods], 2)
							EObjOP("drillEffect", [Mods])

						EObjOP("consumes", [Mods])

						EObjOP("requirements", [Mods])

						if Type == "genericcrafter":
							EObjOP("outputItem", Mods["outputItem"])
						elif Type == "genericsmelter":
							EObjOP("outputLiquid", Mods["outputLiquid"])
						elif Type == "nuclearreactor":
							EObjOP("powerProduction", Mods["powerProduction"], 2)
							EObjOP("itemDuration", Mods["itemDuration"])

						EObjOP("category", [Mods])
						EObjOP("research", [Mods], 2)
						EObjOP("alwaysUnlocked", [Mods])
					elif RootType == "liquids":
						if Type != "":
							EObjOP("type", Type)
							EObj["type"][1].addItem("None")

							ContentObject["Mod"] = DefaultFileSave[RootType][Type]

						else:
							ContentObject["Mod"] = DefaultFileSave[RootType][RootType]

						for s in Mods.keys():
							ContentObject["Mod"][s] = Mods[s]

						Mods = ContentObject["Mod"]
						
						EObjOP("name", [Mods])
						EObjOP("description", [Mods], 0, 120)

						EObjOP("color", [Mods])
						EObjOP("explosiveness", [Mods], 3)
						EObjOP("fliammbility", [Mods])
						EObjOP("radioactivity", [Mods])
						EObjOP("hardness", [Mods], 2)
						EObjOP("cost", [Mods])

						EObjOP("viscosity", [Mods])
						EObjOP("heatCapacity", [Mods])
						EObjOP("effect", [Mods])
						EObjOP("lightColor", [Mods])

						EObjOP("research", [Mods], 2)
						EObjOP("alwaysUnlocked", [Mods])
					else:
						SummonMessage("Главный Тип " + RootType + " не используетса!")

				
			else:
				pass
		#except Exception as x:
			#CloseContentObject()
			#SummonMessage(("OpenContentObjectGUI: " + str(x)), "error")
			#SummonMessage(("Mod: " + str(Mods)), "error")
			




	CloseContentObject()

	

	def OpenPreContentObject():
		Mods = ContentObject["Mod"]
		Type = ContentObject["Type"][1].lower()
		RootType = ContentObject["Type"][0].lower()
		_path = ContentObject["Path"]
		_text = ContentObject["Text"]

		print("=====")
		print(RootType)
		print(Type)
		print("=====")



		SaveObj.show()
		CloseObj.show()

		Name_Content.show()
		Desc_Content.show()

		try:
			if RootType == "mod":
				if "displayName" in Mods:
					Name_Content.setText(coloritaText(Mods["displayName"]))
				else:
					Name_Content.setText(coloritaText(Mods["name"]))
			else:
				Name_Content.setText(coloritaText(Mods["name"]))
		except Exception:
			Name_Content.setText("")
		try:
			Desc_Content.setText(coloritaText(Mods["description"]))
		except Exception:
			Desc_Content.setText("")


		_ttt = ["name", "version", "author"]
		for p in range(len(_ttt)):
			try:
				if "displayName" in RootMod[0] and _ttt[p] == "name":
					_ttt[p] = coloritaText(str(RootMod[0]["displayName"]))
				else:
					_ttt[p] = coloritaText(str(RootMod[0][_ttt[p]]))
			except:
				_ttt[p] = coloritaText("[red]None")

		ModContentFrame.setAllText(_ttt[0], _ttt[1], _ttt[2])
		

		ImageObj = None

		try:
			if Type == "drill":
				if os.path.exists(ImagOPT(toPng(os.path.basename(_path)))):
					ImageObj = Image.open(ImagOPT(toPng(os.path.basename(_path))))
					ImageObj1 = ImageObj.copy()
				else:
					ImageObj = Image.open("resources/icons/error.png")
				if os.path.exists(ImagOPT(toPng(os.path.basename(_path), "-rotator"))):
					_tempImg = Image.open(ImagOPT(toPng(os.path.basename(_path), "-rotator")))
				else:
					ImageObj = Image.open("resources/icons/error.png")
				ImageObj1.paste(_tempImg, (0, 0), _tempImg)
				if os.path.exists(ImagOPT(toPng(os.path.basename(_path), "-top"))):
					_tempImg = Image.open(ImagOPT(toPng(os.path.basename(_path), "-top")))
				else:
					ImageObj = Image.open("resources/icons/error.png")
				ImageObj1.paste(_tempImg, (0, 0), _tempImg)
				ImageObj = ImageObj1
			elif ContentObject["Type"][0] == "mod":
				if os.path.exists(RootMod[1] + "/icon.png"):
					ImageObj = Image.open(RootMod[1] + "/icon.png")
			else:
				if os.path.exists(ImagOPT(toPng(os.path.basename(_path)))):
					ImageObj = Image.open(ImagOPT(toPng(os.path.basename(_path))))

			ImageObj = pillowToPixmap(ImageObj)
			EObj["img"].setPixmap(ImageObj)
		except Exception:
			ImageObj = Image.open("resources/icons/error.png")
			ImageObj = pillowToPixmap(ImageObj)
			EObj["img"].setPixmap(ImageObj)
		
		EObj["img"].show()
		
		EObj["img"].setGeometry(303, 3, 75 - 6, 75 - 6)

		EObj["img"].setScaledContents(True)
		
		EObj["img"].setStyleSheet("border-style: solid; border-width: 3px; border-color: #ffd37f;")

	def EntryObj(Mods, Type = [None, None], _path = None, _text = ""):
		global ContentObject, EditRoot
		CloseContentObject()
		ContentObject["Mod"] = Mods
		ContentObject["Type"][1] = str(Type[1]).lower()
		ContentObject["Type"][0] = str(Type[0]).lower()

		print(ContentObject["Type"][0])
		
		ContentObject["Path"] = _path
		ContentObject["Text"] = _text

		print("=====")
		print(Type)
		print("=====")


		#try:
		if 0==0:
			OpenPreContentObject()

			if EditRoot[0] == 0:
				OpenContentObjectGUI()
			else:
				OpenContentObjectText()
		#except Exception:
		#	pass

		

			

	WS = 0
	
	def SaveButton():
		pass


		
	def SelLCpod(index = None, Type = None):
		if index != None:
			print(tree.model().filePath(index))
			TempMod = openFiler(tree.model().filePath(index))
			#TempMod[0] = json.loads(json.dumps(TempMod[0]))
			
			if TempMod != None:
				if "type" in TempMod[0]:
					
					EntryObj(TempMod[0], [EditRoot[1], TempMod[0]["type"]], tree.model().filePath(index), TempMod[1])
				else:
					EntryObj(TempMod[0], [EditRoot[1], ""], tree.model().filePath(index), TempMod[1])
		if Type != None:
			if Type == "mod":

				_trep = ""
				if os.path.exists(RootMod[1] + "/mod.json"):
					_trep = "json"
				if os.path.exists(RootMod[1] + "/mod.hjson"):
					_trep = "hjson"

				TempModI = openFiler(RootMod[1] + "/" + Type + "." + _trep)
				#TempModI[0] = json.loads(json.dumps(TempModI[0]))
				
				EntryObj(TempModI[0], ["mod", _trep], RootMod[1] + "/" + Type + "." + _trep, TempModI[1])

	
	def SelLC(index = None, event = None, Type = None):
		global WS, RootMod, EditRoot, TempMod, window
		try:
			print("=====")
			print(Type)
			print("=====")
			_yes = False
			if RootMod[1] != "":
				if index != None:
					if os.path.isfile(tree.model().filePath(index)):
						_yes = True
				else:
					_yes = True
				if _yes:
					if TempMod == None or GetContentObjectData() == TempMod:

						SelLCpod(index, Type)

					else:
						msgBox = QMessageBox(window)
						#msgBox.setIcon(QMessageBox.Information)
						msgBox.setText("Сохранить?")
						msgBox.setWindowTitle("Екстреное Сохронение (Test)")
						msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
						#msgBox.buttonClicked.connect(SaveButton)

						SaveDialog = msgBox.exec()
						if SaveDialog == QMessageBox.StandardButton.Yes:
							ModSave()
							SelLCpod(index, Type)
						elif SaveDialog == QMessageBox.StandardButton.No:
							SelLCpod(index, Type)
						elif SaveDialog == QMessageBox.StandardButton.Cancel:
							pass

		except Exception as x:
			SummonMessage(x, "error")
			


	tree.doubleClicked.connect(SelLC)












	# for i in range(0, len(ContentL)):
	# 	ListContent.append([Frame(frame)])
	# 	Temp = ImagOPT(toPng(ContentL1[i]))
	# 	Temp = Image.open(Temp)
	# 	Temp = Temp.resize((18, 18))
	# 	Temp = ImageTk.PhotoImage(Temp)

	# 	ListContent[i].append(Label(ListContent[i][0], image = Temp, width = 18, height = 18))
	# 	ListContent[i][1].image = Temp
	# 	ListContent[i][1].pack(side=LEFT)
	# 	ListContent[i].append(Label(ListContent[i][0], text = str(openFiler(ContentL[i])["name"])).pack(side=LEFT))
	# 	ListContent[i].append(Button(ListContent[i][0], text = "Открыть", command = lambda: openObj(ContentL[i])).pack(side=LEFT))
	# 	ListContent[i].append(Button(ListContent[i][0], text = "Удалить").pack(side=LEFT))
	# 	testAdd(ContentL)



	# 	ListContent[i][0].pack()



	#window.withdraw()
	#window.deiconify()



	window.show()
	window.setBaseSize(800, 700)

	app.exec()


MainL()
