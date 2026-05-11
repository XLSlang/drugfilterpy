from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski
from pydantic import BaseModel
from typing import List


class Molecule(BaseModel):
    smiles: str
    mw: float
    logp: float
    hbd: int
    hba: int
    rot_bonds: int
    pass_rules: bool
    alert_count: int


class Calculator:
    def __init__(self):
        # 警示结构模式
        self.alert_patterns = ["N=N", "N=O", "S(=O)", "P(=O)"]
    
    def parse_smiles(self, smiles: str) -> Molecule:
        """解析单个SMILES"""
        mol = Chem.MolFromSmiles(smiles)
        
        if mol is None:
            # 无效SMILES返回空数据
            return Molecule(
                smiles=smiles,
                mw=0,
                logp=0,
                hbd=0,
                hba=0,
                rot_bonds=0,
                pass_rules=False,
                alert_count=0
            )
        
        # 计算分子性质
        mw = Descriptors.MolWt(mol)
        logp = Descriptors.MolLogP(mol)
        hbd = Lipinski.NumHDonors(mol)
        hba = Lipinski.NumHAcceptors(mol)
        rot_bonds = Descriptors.NumRotatableBonds(mol)
        
        # 检查Lipinski规则
        pass_rules = self._check_lipinski(mw, logp, hbd, hba, rot_bonds)
        
        # 检查警示结构
        alert_count = self._check_alerts(smiles)
        
        return Molecule(
            smiles=smiles,
            mw=round(mw, 1),
            logp=round(logp, 2),
            hbd=hbd,
            hba=hba,
            rot_bonds=rot_bonds,
            pass_rules=pass_rules,
            alert_count=alert_count
        )
    
    def process_batch(self, smiles_list: List[str]) -> List[Molecule]:
        """批量处理"""
        results = []
        for smiles in smiles_list:
            smiles = smiles.strip()
            if smiles:
                results.append(self.parse_smiles(smiles))
        return results
    
    def _check_lipinski(self, mw: float, logp: float, hbd: int, hba: int, rot_bonds: int) -> bool:
        """检查Lipinski五规则"""
        # mw ≤ 500, logP ≤ 5, HBD ≤ 5, HBA ≤ 10, RotBonds ≤ 10
        return mw <= 500 and logp <= 5 and hbd <= 5 and hba <= 10 and rot_bonds <= 10
    
    def _check_alerts(self, smiles: str) -> int:
        """检查警示结构"""
        count = 0
        for pattern in self.alert_patterns:
            if pattern in smiles:
                count += 1
        return count