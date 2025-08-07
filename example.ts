import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://www.douyin.com/?recommend=1');
  await page.getByRole('button', { name: '登录' }).click();
  await page.locator('div').filter({ hasText: /^手机刷脸验证需\*荣本人操作$/ }).first().click();
  await page.goto('https://www.douyin.com/?recommend=1');
  await page.getByText('保存', { exact: true }).click();
  await page.locator('.GqFbCFGv').click();
  await page.getByText('开启读屏标签读屏标签已关闭精选推荐AI抖音关注8').press('ArrowDown');
  await page.getByText('开启读屏标签读屏标签已关闭精选推荐AI抖音关注8').press('ArrowDown');
  await page.locator('.nM3w4mVK').click();
  await page.locator('.nM3w4mVK').click();
  await page.getByText('开启读屏标签读屏标签已关闭精选推荐AI抖音关注8').press('ArrowDown');
  await page.getByText('开启读屏标签读屏标签已关闭精选推荐AI抖音关注8').press('ArrowDown');
  await page.locator('#douyin-web-download-guide-container').getByRole('img').nth(2).click();
  await page.locator('.eJhYZuIF > div:nth-child(2)').press('ArrowDown');
  await page.locator('.eJhYZuIF > div:nth-child(2)').press('ArrowDown');
  await page.locator('.eJhYZuIF > div:nth-child(2)').press('ArrowDown');
  await page.locator('.eJhYZuIF > div:nth-child(2)').press('ArrowDown');
  await page.locator('.eJhYZuIF > div:nth-child(2)').press('ArrowDown');
  await page.locator('.eJhYZuIF > div:nth-child(2)').press('ArrowDown');
  await page.locator('.eJhYZuIF > div:nth-child(2)').press('ArrowDown');
  await page.locator('.eJhYZuIF > div:nth-child(2)').press('ArrowDown');
  await page.locator('.eJhYZuIF > div:nth-child(2)').press('ArrowDown');
  await page.locator('.eJhYZuIF > div:nth-child(2)').press('ArrowDown');
  await page.locator('.jp8u3iov > div > svg').click();
  await page.locator('.eJhYZuIF > div:nth-child(2)').press('ArrowDown');
  await page.locator('.DnsmeHpw').click();
  await page.getByText('开启读屏标签读屏标签已关闭精选推荐AI抖音关注8').press('ArrowDown');
  await page.getByText('开启读屏标签读屏标签已关闭精选推荐AI抖音关注8').press('ArrowDown');
  await page.locator('video').nth(1).click({
    button: 'right'
  });
  await page.locator('div').filter({ hasText: /^不感兴趣$/ }).first().click();
  await page.locator('video').nth(1).click({
    button: 'right'
  });
  await page.getByText('不感兴趣（R）').click();
  await page.getByText('3.0万').click();
});