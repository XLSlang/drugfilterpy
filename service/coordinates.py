from rdkit import Chem
from rdkit.Chem import AllChem
from typing import List, Tuple
import math


class Atom:
    def __init__(self, element: str, index: int):
        self.element = element
        self.index = index


class Structure3D:
    def __init__(self, atoms: List[Atom], coords: List[List[float]], bonds: List[Tuple[int, int]]):
        self.atoms = atoms
        self.coords = coords
        self.bonds = bonds


class CoordinateGenerator:
    def __init__(self):
        pass
    
    def generate_3d(self, smiles: str) -> Structure3D:
        """生成3D结构"""
        mol = Chem.MolFromSmiles(smiles)
        
        if mol is None:
            return Structure3D(atoms=[], coords=[], bonds=[])
        
        # 添加氢原子
        mol = Chem.AddHs(mol)
        
        # 生成3D构象
        AllChem.EmbedMolecule(mol, randomSeed=42)
        AllChem.MMFFOptimizeMolecule(mol)
        
        # 获取原子坐标
        conf = mol.GetConformer()
        atoms = []
        coords = []
        
        for i, atom in enumerate(mol.GetAtoms()):
            element = atom.GetSymbol()
            pos = conf.GetAtomPosition(i)
            atoms.append(Atom(element=element, index=i))
            coords.append([pos.x, pos.y, pos.z])
        
        # 获取化学键
        bonds = []
        for bond in mol.GetBonds():
            begin_idx = bond.GetBeginAtomIdx()
            end_idx = bond.GetEndAtomIdx()
            bonds.append((begin_idx, end_idx))
        
        # 居中并缩放到合适范围
        coords = self._center_and_scale(coords)
        
        return Structure3D(atoms=atoms, coords=coords, bonds=bonds)
    
    def _center_and_scale(self, coords: List[List[float]]) -> List[List[float]]:
        """居中并缩放到合适大小"""
        if not coords:
            return coords
        
        # 计算中心点
        center = [0.0, 0.0, 0.0]
        for p in coords:
            center[0] += p[0]
            center[1] += p[1]
            center[2] += p[2]
        n = len(coords)
        center = [c / n for c in center]
        
        # 平移到原点
        for p in coords:
            p[0] -= center[0]
            p[1] -= center[1]
            p[2] -= center[2]
        
        # 计算最大半径并缩放
        max_dist = 0.0
        for p in coords:
            dist = math.sqrt(p[0]**2 + p[1]**2 + p[2]**2)
            max_dist = max(max_dist, dist)
        
        if max_dist > 0:
            scale = 2.5 / max_dist
            for p in coords:
                p[0] *= scale
                p[1] *= scale
                p[2] *= scale
        
        return coords