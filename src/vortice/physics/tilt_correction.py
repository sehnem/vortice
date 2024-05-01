import numpy as np

# Constants
p = np.pi
error = float('nan')

# Functions
def YawMtx(DirYaw):
    CosTheta = np.cos(p * DirYaw / 180.0)
    SinTheta = np.sin(p * DirYaw / 180.0)
    Yaw = np.array([
        [CosTheta, SinTheta, 0.0],
        [-SinTheta, CosTheta, 0.0],
        [0.0, 0.0, 1.0]
    ])
    return Yaw


def PitchMtx(DirPitch):
    CosPhi = np.cos(p * DirPitch / 180.0)
    SinPhi = np.sin(p * DirPitch / 180.0)
    Pitch = np.array([
        [CosPhi, 0.0, SinPhi],
        [0.0, 1.0, 0.0],
        [-SinPhi, 0.0, CosPhi]
    ])
    return Pitch


def RollMtx(DirRoll):
    CosPsi = np.cos(p * DirRoll / 180.0)
    SinPsi = np.sin(p * DirRoll / 180.0)
    Roll = np.array([
        [1.0, 0.0, 0.0],
        [0.0, CosPsi, SinPsi],
        [0.0, -SinPsi, CosPsi]
    ])
    return Roll


# Subroutines
def TiltCorrection(RotMeth, GoPlanarFit, Set, nrow, ncol, nsec, printout):
    DirYaw = np.array([error])
    DirPitch = np.array([error])
    DirRoll = np.array([error])

    if printout:
        print(f"Performing tilt correction by: {RotMeth}")

    # Set errors if any component has error
    if np.any(np.isnan(Set)):
        Set[:, :] = error

    if RotMeth.strip() == 'double_rotation':
        DirYaw, DirPitch = DoubleRotation(Set)
    elif RotMeth.strip() == 'triple_rotation':
        DirYaw, DirPitch = DoubleRotation(Set)
        DirRoll = ThirdRotation(Set)
    elif RotMeth.strip() in ['planar_fit', 'planar_fit_no_bias']:
        WindSec = round(error)
        if WindSec != error:
            if GoPlanarFit[WindSec]:
                DirYaw = PlanarFitByWindSector(WindSec, Set)
            else:
                DirYaw, DirPitch = DoubleRotation(Set)
        else:
            DirYaw, DirPitch = DoubleRotation(Set)

    if printout:
        print("Done.")

    return DirYaw[0], DirPitch[0], DirRoll[0]


def DoubleRotation(Set):
    nrow, ncol = Set.shape
    Mean = np.nanmean(Set, axis=0)

    SinTheta = Mean[1] / np.sqrt(Mean[0] ** 2 + Mean[1] ** 2)
    CosTheta = Mean[0] / np.sqrt(Mean[0] ** 2 + Mean[1] ** 2)
    DirYaw = 180.0 * np.arccos(CosTheta) / p
    if SinTheta < 0.0:
        DirYaw = 360.0 - DirYaw

    Yaw = YawMtx(DirYaw)

    for i in range(nrow):
        if not np.isnan(Set[i, :3]).any():
            Set[i, :3] = np.matmul(Yaw, Set[i, :3])

    Mean = np.nanmean(Set, axis=0)

    SinPhi = Mean[2] / np.sqrt(Mean[0] ** 2 + Mean[2] ** 2)
    DirPitch = 180.0 * np.arcsin(SinPhi) / p

    Pitch = PitchMtx(DirPitch)

    for i in range(nrow):
        if not np.isnan(Set[i, :3]).any():
            Set[i, :3] = np.matmul(Pitch, Set[i, :3])

    return DirYaw, DirPitch


def ThirdRotation(Set):
    nrow, ncol = Set.shape
    Mean = np.nanmean(Set, axis=0)
    Cov = np.cov(Set.T)

    Dum1 = 2.0 * Cov[1, 2]
    Dum2 = Cov[1, 1] - Cov[2, 2]

    if Dum2 == 0:
        return error  # No valid rotation

    Dumm = Dum1 / Dum2
    DirRoll = (0.5 * np.arctan(Dumm)) * 180.0 / p

    if abs(DirRoll) < 10.0:
        Roll = RollMtx(DirRoll)

        for i in range(nrow):
            if not np.isnan(Set[i, :3]).any():
                Set[i, :3] = np.matmul(Roll, Set[i, :3])

    return DirRoll


def PlanarFitByWindSector(WindSec, Set):
    nrow, ncol = Set.shape
    Mean = np.nanmean(Set, axis=0)

    if WindSec == round(error):
        return error

    Mat = PFMat[:, :, WindSec]  # Ensure PFMat is defined in your scope

    for i in range(nrow):
        if not np.isnan(Set[i, :3]).any():
            Set[i, :3] = np.matmul(Mat, Set[i, :3])

    Mean = np.nanmean(Set, axis=0)

    SinTheta = Mean[1] / np.sqrt(Mean[0] ** 2 + Mean[1] ** 2)
    CosTheta = Mean[0] / np.sqrt(Mean[0] ** 2 + Mean[1] ** 2)

    DirYaw = 180.0 * np.arccos(CosTheta) / p
    if SinTheta < 0.0:
        DirYaw = 360.0 - DirYaw

    Yaw = YawMtx(DirYaw)

    for i in range(nrow):
        if not np.isnan(Set[i, :3]).any():
            Set[i, :3] = np.matmul(Yaw, Set[i, :3])

    return DirYaw
