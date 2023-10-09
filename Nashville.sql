Select *
From PortfolioProject.dbo.Nashville

-- Standardizacija

Select SaleDate, CONVERT(Date,SaleDate)
From PortfolioProject.dbo.Nashville

Update Nashville
SET SaleDateConverted = CONVERT(Date, SaleDate)


-- Populate Proprety Address

Select *
From PortfolioProject.dbo.Nashville
Where PropertyAddress is null
order by ParcelID

Select a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress, ISNULL(a.PropertyAddress, b.PropertyAddress)
From PortfolioProject.dbo.Nashville a
JOIN PortfolioProject.dbo.Nashville b
	on a.ParcelID = b.ParcelID
	AND a.[UniqueID ] <> b.[UniqueID ]
Where a.PropertyAddress is null

Update a
SET PropertyAddress = ISNULL(a.PropertyAddress, b.PropertyAddress)

From PortfolioProject.dbo.Nashville a
JOIN PortfolioProject.dbo.Nashville b
	on a.ParcelID = b.ParcelID
	AND a.[UniqueID ] <> b.[UniqueID ]
Where a.PropertyAddress is null


-- Breaking out Address into Individual Colums (Address, City, State)

Select PropertyAddress
From PortfolioProject..Nashville

SELECT
SUBSTRING(PropertyAddress, 1, CHARINDEX(',',PropertyAddress) -1) as Address
, SUBSTRING(PropertyAddress, CHARINDEX(',',PropertyAddress) +1, LEN(PropertyAddress)) as City


From PortfolioProject..Nashville

ALTER TABLE Nashville
Add ProprertySplitAddress Nvarchar(255);

Update Nashville
SET ProprertySplitAddress = SUBSTRING(PropertyAddress, 1, CHARINDEX(',',PropertyAddress) -1)

ALTER TABLE Nashville
Add ProprertySplitCity Nvarchar(255);

Update Nashville
SET ProprertySplitCity = SUBSTRING(PropertyAddress, CHARINDEX(',',PropertyAddress) +1, LEN(PropertyAddress))

Select *
From PortfolioProject.dbo.Nashville

 Select OwnerAddress
From PortfolioProject.dbo.Nashville

Select
PARSENAME(REPLACE(OwnerAddress,',','.'),3)
, PARSENAME(REPLACE(OwnerAddress,',','.'),2)
, PARSENAME(REPLACE(OwnerAddress,',','.'),1)
From PortfolioProject.dbo.Nashville

ALTER TABLE Nashville
Add OwnerSplitAddress Nvarchar(255);

Update Nashville
SET OwnerSplitAddress = PARSENAME(REPLACE(OwnerAddress,',','.'),3)

ALTER TABLE Nashville
Add OwnerSplitCity Nvarchar(255);

Update Nashville
SET OwnerSplitCity = PARSENAME(REPLACE(OwnerAddress,',','.'),2)

ALTER TABLE Nashville
Add OwnerSplitState Nvarchar(255);

Update Nashville
SET OwnerSplitState = PARSENAME(REPLACE(OwnerAddress,',','.'),1)

Select *
From PortfolioProject.dbo.Nashville

Select Distinct(SoldAsVacant), Count(SoldAsVacant)
From PortfolioProject..Nashville
Group by SoldAsVacant
order by 2

Select SoldAsVacant,
 CASE When SoldAsVacant = 'Y' THEN 'Yes'
	  When SoldAsVacant = 'N' THEN 'no'
	  ELSE SoldAsVacant
	  END
From PortfolioProject.dbo.Nashville

Update Nashville
SET SoldAsVacant = CASE When SoldAsVacant = 'Y' THEN 'Yes'
	  When SoldAsVacant = 'N' THEN 'no'
	  ELSE SoldAsVacant
	  END

Select *
From PortfolioProject..Nashville


-- Remove Duplicates

WITH RowNumCTE AS(
Select *,
	ROW_NUMBER() OVER(
	PARTITION BY ParcelID, 
				 PropertyAddress,
				 SalePrice,
				 SaleDate,
				 LegalReference
				 ORDER BY
					UniqueID
					) row_num
From PortfolioProject..Nashville
)
-- DELETE umesto Select *
Select *
From RowNumCTE
Where row_num>1
order by PropertyAddress



-- Delete Unused Columns

Select *
From PortfolioProject..Nashville

ALTER TABLE PortfolioProject..Nashville
 DROP COLUMN OwnerAddress, TaxDistrict, PropertyAddress

 ALTER TABLE PortfolioProject..Nashville
 DROP COLUMN  SaleDate